class DebugHandler:
    def __init__(self, name):
        self.name = name
        self.debug = False

    def print(self, message):
        if self.debug:
            print(f"{self.name}: {message}")

    # Debug Print Function
    def dprint(self, *args):
        if self.debug:
            print(f"{self.name}: ", *args)

    # Debug Print Function with System Flash Memory
    def print_system_df(self):
        if self.debug:
            try:
                import os

                # Get the filesystem information
                s_info = os.statvfs("/")

                # Calculate the total, used, and free space
                total = s_info[0] * s_info[2]
                free = s_info[0] * s_info[3]
                used = total - free

                # Print the information
                print(f"Total: {total} bytes")
                print(f"Used: {used} bytes")
                print(f"Free: {free} bytes")
            except Exception as e:
                self.dprint("Error in print_system_df:", e)
