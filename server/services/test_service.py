class Test:
    def push(self, thing):
        print(thing)
        return True

    def get(self):
        print("get")
        return [
            {
                'id': 1,
                'name': "A"
            },
            {
                'id': 2,
                'name': "B"
            }
        ]

    def delete(self, id: int):
        print(id)
        return True
