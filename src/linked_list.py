class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node

    def delete_node_by_index(self, index):
        if index < 0:
            print("Index cannot be negative")
            return

        curr = self.head
        if index == 0:
            if self.head:
                self.head = curr.next
                curr = None
            return

        prev = None
        count = 0
        while curr and count != index:
            prev = curr
            curr = curr.next
            count += 1

        if curr is None:
            print("Index out of range")
            return

        prev.next = curr.next
        curr = None

    def reverse(self):
        prev = None
        curr = self.head
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        self.head = prev

    def sort(self, order='asc'):
        if not self.head:
            return
        values = []
        curr = self.head
        while curr:
            values.append(curr.value)
            curr = curr.next
        values.sort(reverse=(order == 'desc'))
        self.head = None
        for value in values:
            self.add_node(value)

    @staticmethod
    def merge(*linked_lists):
        merged_list = LinkedList()
        for temp in linked_lists:
            curr = temp.head
            while curr:
                merged_list.add_node(curr.value)
                curr = curr.next
        return merged_list
