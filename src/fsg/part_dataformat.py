class PartFormData:
    def __init__(
        self,
        system=None,
        assembly="Other",
        assembly_name=None,
        assembly_comment="TODO",
        sub_assembly="- none -",
        sub_assembly_name=None,
        part=None,
        makebuy="b",
        comments="TODO",
        quantity=1,
        custom_id=None,
    ):
        """
        Initializes an instance of the class with the provided parameters.

        Parameters:
            system (str, optional): The system identifier, e.g., 'BR', 'EL', 'EN', 'FR', 'SU', 'ST', 'WT', 'MS',.
            assembly (str, optional): The assembly name of already existing Assemblies, e.g., 'Brake Discs', 'Brake Fluid', etc.
            assembly_name (str, optional): Optional field for the assembly name when the Assembly is not a default Assembly in the FSG Tool. F. ex. 'Other: Front Brake', 'Other: Assembly' .
            assembly_comment (str, optional): Optional comment for a non default assembly.
            sub_assembly (str, optional): Optional sub-assembly selection. Defaults to '- none -'
            sub_assembly_name (str, optional): Optional sub-assembly name. Defaults to None
            part (str, optional): Text input for the part.
            makebuy (str, optional): 'm' for make, 'b' for buy (radio button).
            comments (str, optional): Optional comments field.
            quantity (int, optional): Number of parts to enter.
            custom_id (str, optional): Optional custom ID field (maxlength=15).
        """
        self.system: str = system
        self.assembly: str = assembly
        self.assembly_name: str = assembly_name
        self.assembly_comment: str = assembly_comment
        self.sub_assembly: str = sub_assembly
        self.sub_assembly_name: str = sub_assembly_name
        self.part: str = part
        self.makebuy: str = makebuy
        self.comments: str = comments
        self.quantity: int = quantity
        self.custom_id: str = custom_id

    def __repr__(self):
        """
        Provide a string representation of the PartFormData object.

        Returns:
            str: A string that includes the system, assembly, assembly_name, assembly_comment,
                 sub_assembly, sub_assembly_name, part, makebuy, comments, and quantity attributes
                 of the PartFormData object.
        """
        return (
            f"PartFormData(system={self.system}, assembly={self.assembly}, assembly_name={self.assembly_name}, "
            f"assembly_comment={self.assembly_comment}, sub_assembly={self.sub_assembly}, "
            f"sub_assembly_name={self.sub_assembly_name}, part={self.part}, makebuy={self.makebuy}, "
            f"comments={self.comments}, quantity={self.quantity})"
        )
