class Stack:
    """Class representing a Stack data structure using Python list (LIFO)."""

    def __init__(self, capacity=None):
        self.items = []
        self.capacity = capacity  # Optional maximum size for the stack

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self.items) == 0

    def is_full(self):
        """Check if the stack has reached maximum capacity."""
        if self.capacity is None:
            return False
        return len(self.items) >= self.capacity

    def push(self, item):
        """Push an element onto the top of the stack."""
        if self.is_full():
            print(f"Stack Overflow! Cannot push '{item}'. Stack is full.")
            return False
        self.items.append(item)
        print(f"Pushed: {item}")
        return True

    def pop(self):
        """Remove and return the top element from the stack."""
        if self.is_empty():
            print("Stack Underflow! Stack is empty.")
            return None
        popped_item = self.items.pop()
        print(f"Popped: {popped_item}")
        return popped_item

    def peek(self):
        """Return the top element without removing it."""
        if self.is_empty():
            print("Stack is empty. No top element.")
            return None
        print(f"Top element: {self.items[-1]}")
        return self.items[-1]

    def size(self):
        """Return the total number of elements in the stack."""
        print(f"Current Stack Size: {len(self.items)}")
        return len(self.items)

    def display(self):
        """Display the elements in the stack from top to bottom."""
        if self.is_empty():
            print("Stack is empty: []")
        else:
            print("\n--- Stack (Top -> Bottom) ---")
            for item in reversed(self.items):
                print(f"| {item} |")
            print("-----------------------------\n")


def main():
    print("=== Interactive Stack Data Structure ===")
    
    # Optional capacity limit
    choice_cap = input("Do you want to set a maximum capacity for the stack? (y/n): ").strip().lower()
    capacity = None
    if choice_cap == 'y':
        try:
            capacity = int(input("Enter maximum stack capacity: "))
            if capacity <= 0:
                print("Invalid capacity! Defaulting to unlimited capacity.")
                capacity = None
        except ValueError:
            print("Invalid input! Defaulting to unlimited capacity.")

    stack = Stack(capacity=capacity)

    while True:
        print("\n--- Stack Operations ---")
        print("1. Push")
        print("2. Pop")
        print("3. Peek (Top Element)")
        print("4. Check if Empty")
        print("5. Get Stack Size")
        print("6. Display Stack")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            item = input("Enter element to push: ")
            stack.push(item)
        elif choice == '2':
            stack.pop()
        elif choice == '3':
            stack.peek()
        elif choice == '4':
            if stack.is_empty():
                print("Status: Stack is EMPTY.")
            else:
                print("Status: Stack is NOT empty.")
        elif choice == '5':
            stack.size()
        elif choice == '6':
            stack.display()
        elif choice == '7':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice! Please select an option from 1 to 7.")


if __name__ == "__main__":
    main()
