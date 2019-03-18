# from Database import Database
# db = Database()
class Logging():
    # -- Basic text file logging via decorator.
    # -- This should be updated to support logging to sqlite.



    def log(self, tag_name):
        def tags_decorator(func):
            def func_wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                with open("log.txt",'a+') as logfile:
                    logfile.write("{}{}\n".format(tag_name,result ))
                return result
            return func_wrapper
        return tags_decorator


    def __Database_Write__(self, values):
        if type(values) != dict or 'type' not in values or 'data' not in values:
            return False
    # -- Trialing decortator SQL logging
    def log_login(self, tag_name):
        def tags_decorator(func):
            def func_wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                with open("log.txt",'a+') as logfile:
                    logfile.write("{}{}\n".format(tag_name,result ))
                return result
            return func_wrapper
        return tags_decorator

