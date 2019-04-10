
class DashboradMiddleware():
    def process_exception(self, request, exception):
        print(exception.__class__.__name__)
        print(exception.message)
        print('Testin Kiran  .......')
        return None
