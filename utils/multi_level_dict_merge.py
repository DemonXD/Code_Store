import copy
from typing import Any


# class DictKeyError(KeyError):
#     pass


class NotEnoughItemsError(Exception):
    """
    exception for the error about the item account is less
    than 2
    """
    pass


class StructureError(Exception):
    """
    exception for the error about the items in listofdict
    do not have the same structure
    """
    pass


class ItemTypeError(Exception):
    """
    exception for the error about the items in listofdict
    do not have the same structure
    """
    pass


class MergeDictTool:
    """
    @Date:          4/28/2020, 17:11
    @author:        "Miles Xu"
    @copyright:     "Copyright 2020, The DM Project"
    @credits:       ["Miles Xu", ]
    @license:       "MIT"
    @version:       "0.0.1"
    @maintainer:    "Miles Xu"
    @email:         "kanonxmm@163.com"
    @status:        "Development"
    @condition:
        input: list of dict, every dict has the same structure and same keys
    @feature:
        merge multi level dict's value, simple:
        input:
            a = {"field": {"column": {"n1": "v1", "n2": "v2"}}}
            b = {"field": {"column": {"n1": "v3", "n2": "v4"}}}
            c = {"field": {"column": {"n1": "v5", "n2": "v6"}}}

        return:
            {"field": {"column": {"n1": ["v1", "v3", "v5"],"n2": ["v2", "v4", "v6"]}}}
    """
    def __init__(self, listwithdict: list):
        self.originlist = listwithdict
        self.sampleitem = listwithdict[0] if len(listwithdict) > 1 else None
        self.pathlist = []

    def analysisPath(self, sampleitem: dict, singletemppath: list=None):
        """
        Desc. : according to the sampleitem to analysis all path, base to DFS
        :input sampleitem:
        :input singletemppath:
        :return : self.pathlist -> 
            [["field", "column", "n1"], ["field", "column", "n2"], [...] ...]
        """
        if not sampleitem:
            raise NotEnoughItemsError
        elif not isinstance(sampleitem, dict):
            raise ItemTypeError
        else:
            for key, val in sampleitem.items():
                singlepath = copy.deepcopy(singletemppath) if singletemppath is not None else []
                if isinstance(val, dict):
                    singlepath.append(key)
                    self.analysisPath(val, singlepath)
                else:
                    singlepath.append(key)
                    self.pathlist.append(singlepath)

    
    def buildblankdict(self, res: dict):
        """
        Desc. : according to self.pathlist to build a blank dict
        :input res: origin dict
        :return : dict of cleared value
        """
        for key, val in res.items():
            if not isinstance(val, dict):
                res[key] = []
            else:
                res[key] = self.buildblankdict(val)
        return res

    def getPathValue(self, singleitem: dict, path: list) -> Any:
        """
        :input singleitem: the item of listwithdict
        :input path: the list of key, like: ["field", "column", "n1"]
        :return : return the value of input path in singleitem
        """
        temp = None
        for each_key in path:
            if not temp:
                temp = singleitem.get(each_key)
                continue
            temp = temp.get(each_key)
            if not temp: # if each item structure not equal, raise exception
                raise StructureError
        return temp

    def setPathvalue(self, result: dict, path: list, value: Any):
        """
        Desc. : fill the value to the specified path of result
        :input result: origin dict to be filled with value
        :input value: the value to be filled
        """
        temp = None
        for idx, each_key in enumerate(path):
            if not temp:
                temp = result[each_key]
                continue
            if idx+1 == len(path):
                if isinstance(temp[each_key], list):
                    temp[each_key].append(value)
                else:
                    raise ItemTypeError
            temp = temp[each_key]

    def mergeAndCalculate(self):
        self.analysisPath(self.sampleitem)
        if self.pathlist is not []:
            # print(self.pathlist)
            result = self.buildblankdict(copy.deepcopy(self.sampleitem))
            print("blank dict: ", result)
            for each_item in self.originlist:
                for each_path in self.pathlist:
                    value = self.getPathValue(each_item, each_path) # get each path value
                    self.setPathvalue(result, each_path, value)
            print("result dict: ", result)


if __name__ == "__main__":
    sample = [
        {
            "field": {
                "column1": {
                    "n1": {"m1": "v1"}, 
                    "n2": "v2"
                }, 
                "column2": "v~"
            }
        },
        {
            "field": {
                "column1": {
                    "n1": {"m1": "v3"}, 
                    "n2": "v4"}, 
                "column2": "v^"
            }
        },
        {
            "field": {
                "column1": {
                    "n1": {"m1": "v5"}, 
                    "n2": "v6"}, 
                "column2": "v*"
            }
        },
    ]
    sample2 = [
        {
            "field": {
                "column1": {
                    "n1": {"m1": "v1"}, 
                    "n2": "v2"
                }, 
                "column2": {"n3": "v~"}
            }
        },
        {
            "field": {
                "column1": {
                    "n1": {"m1": "v3"}, 
                    "n2": "v4"}, 
                "column2": {"n3": "v^"}
            }
        },
        {
            "field": {
                "column1": {
                    "n1": {"m1": "v5"}, 
                    "n2": "v6"}, 
                "column2": {"n3": "v*"}
            }
        },
    ]

    ins = MergeDictTool(sample).mergeAndCalculate()
    ins = MergeDictTool(sample2).mergeAndCalculate()