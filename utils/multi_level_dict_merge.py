"""
@Date: 2020/4/28, 17:11
__author__ = "Miles Xu"
__copyright__ = "Copyright 2020, The DM Project"
__credits__ = ["Miles Xu", ]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Miles Xu"
__email__ = "kanonxmm@163.com"
__status__ = "Development"
@feature:
    merge multi level dict's value, simple:
    a = {"field": {"column": {"n1": "v1", "n2": "v2"}}}
    b = {"field": {"column": {"n1": "v3", "n2": "v4"}}}
    c = {"field": {"column": {"n1": "v5", "n2": "v6"}}}

    return:
        result = {
            "field": {
                "column": {
                    "n1": ["v1", "v3", "v5"],
                    "n2": ["v2", "v4", "v6"]
                }
            }
        }
"""

class MergeDict:
    pass


if __name__ == "__main__":
    print(__doc__)