class FormData:
    def __init__(
        self,
        system=None,
        assembly=None,
        assembly_name=None,
        assembly_comment=None,
        sub_assembly=None,
        sub_assembly_name=None,
        part=None,
        makebuy=None,
        comments=None,
        quantity=None,
        custom_id=None,
    ):
        """
        Initializes an instance of the class with the provided parameters.

        Parameters:
            system (str, optional): The system identifier, e.g., 'BR', 'EL', 'EN', etc.
            assembly (str, optional): The assembly name, e.g., 'Brake Discs', 'Brake Fluid', etc.
            assembly_name (str, optional): Optional field for the assembly name when applicable.
            assembly_comment (str, optional): Optional comments related to the assembly.
            sub_assembly (str, optional): Optional sub-assembly selection.
            sub_assembly_name (str, optional): Optional sub-assembly name.
            part (str, optional): Text input for the part.
            makebuy (str, optional): 'm' for make, 'b' for buy (radio button).
            comments (str, optional): Optional comments field.
            quantity (int, optional): Number of parts to enter.
            custom_id (str, optional): Optional custom ID field (maxlength=15).
        """
        self.system: str = system  # e.g., 'BR', 'EL', 'EN', etc.
        self.assembly: str = assembly  # e.g., 'Brake Discs', 'Brake Fluid', etc.
        self.assembly_name: str = (
            assembly_name  # Optional field for assembly name (when applicable)
        )
        self.assembly_comment: str = (
            assembly_comment  # Optional comments related to the assembly
        )
        self.sub_assembly: str = sub_assembly  # Optional sub-assembly selection
        self.sub_assembly_name: str = sub_assembly_name  # Optional sub-assembly name
        self.part: str = part  # Text input for part
        self.makebuy: str = makebuy  # 'm' for make, 'b' for buy (radio button)
        self.comments: str = comments  # Optional comments field
        self.quantity: int = quantity  # Number of parts to enter
        self.custom_id: str = custom_id  # Optional custom ID field (maxlength=15)

    def __repr__(self):
        """
        Provide a string representation of the FormData object.

        Returns:
            str: A string that includes the system, assembly, assembly_name, assembly_comment,
                 sub_assembly, sub_assembly_name, part, makebuy, comments, and quantity attributes
                 of the FormData object.
        """
        return (
            f"FormData(system={self.system}, assembly={self.assembly}, assembly_name={self.assembly_name}, "
            f"assembly_comment={self.assembly_comment}, sub_assembly={self.sub_assembly}, "
            f"sub_assembly_name={self.sub_assembly_name}, part={self.part}, makebuy={self.makebuy}, "
            f"comments={self.comments}, quantity={self.quantity})"
        )
