class _const:
    class ConstError(TypeError): pass
    class ConstCaseError(ConstError): pass
    
    def __setattr(self,name,value):
        if self.__dict__.has_key(name):
            raise self.ConstError("Can not change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError("const name %s is not all upper" % name)
        self.__dict__[name] = value

const = _const()

const.LOGIN='http://zqbam.creditease.corp/pages/zqActiveUser/loginZqActiveUser.do'
const.SELECT_PLAN_EXECUTION='http://zqbam.creditease.corp/pages/zqPlanexecution/showZqPlanexecution.do'

import sys
sys.modules[__name__] = const