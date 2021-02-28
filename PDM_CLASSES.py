import sys
import inspect

res = {
    "r2Solutn" : {
        "attributes" : {
            "attribute1" : "int",
            "attribute2" : "str",
            "attribute3" : "float",
        }
    }
}

for className,classDict in res.items():
    attributesDict = classDict.get('attributes',{})
    classString = "class {className}:\n".format(className=className)
    classString += " "*4 + "className : str = \"{0}\"\n".format(className)
    attributeTypes = []
    for attribute,attributeType in attributesDict.items():
        classString += " "*4 + "{0} : {1} = \"{0}\"\n".format(attribute,attributeType)
        attributeTypes.append("\"{0}\" : {1}".format(attribute,attributeType))
    classString += " "*4 + "ATTRIBUTE_TYPES = {{ {0} }}".format(" , ".join(attributeTypes))

class r2Solutn:
    className : str = "r2Solutn"
    attribute1 : int = "attribute1"
    attribute2 : str = "attribute2"
    attribute3 : float = "attribute3"
    ATTRIBUTE_TYPES = { "attribute1" : int , "attribute2" : str , "attribute3" : float }

def queryClass(**kwargs):
    className           = kwargs.get('className')
    classObj            = getattr(sys.modules[__name__], className)
    allowedAttributes   = []
    for attribute in classObj.ATTRIBUTE_TYPES.keys():
        for customSupport in [ attribute+x for x in ["","__like","__not_like","__in",
        "__not_in","__not","__gt","__gte","__lt","__lte"]]:
            allowedAttributes.append(customSupport)
    mathOperators = {"__gt" : ">",'__gte' : ">=", "__lt": "<", "__lte": "<=" }
    kwargs      = { k: v for k,v in kwargs.items() if k in allowedAttributes }
    queries     = []
    for attribute,value in kwargs.items():
        operator = "="
        if attribute.endswith("__like") or attribute.endswith("__not_like"):
            operator    = "LIKE" if attribute.endswith("__like") else "NOT LIKE"
            attribute   = attribute.strip("__like").strip("__not_like")
            value       = "\"{0}\"".format(value)
        elif attribute.endswith("__in") or attribute.endswith("__not_in"):
            operator    = "IN" if attribute.endswith("__in") else "NOT IN"
            attribute   = attribute.strip("__in").strip("__not_in")
            value       = list(map(lambda x: classObj.ATTRIBUTE_TYPES[attribute](x),value))
            if classObj.ATTRIBUTE_TYPES[attribute] == str:
                value = ["\"{0}\"".format(str(x)) for x in value]
            else:
                value = [ str(x) for x in value ]
            value       = " , ".join(value)
            value       = "({0})".format(value)
        elif attribute.endswith("__not"):
            operator = "<>"
        elif any(map(lambda x: attribute.endswith(x),mathOperators.keys())):
            for mathOperator in mathOperators.keys():
                if attribute.endswith(mathOperator): operator = mathOperators.get(mathOperator)
            for mathOperator in mathOperator.keys():
                attribute = attribute.strip(mathOperator)
            value = classObj.ATTRIBUTE_TYPES[attribute](value)
        queries.append("{attribute} {operator} {value}".format(
            attribute=attribute,
            operator=operator,
            value=value
        ))
    sqlQuery = "QueryWhere3({0})".format(" AND ".join(queries))
    return sqlQuery

res = queryClass(className=r2Solutn.className,attribute2__in=[45,46],attribute2__like="Test%",attribute3=45)
print(res)