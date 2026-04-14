import ast
class Utils: 
    @staticmethod
    def parse(x: str):
            if isinstance(x,str):
                  return ast.literal_eval(x)
            else: 
                  return []
    
            