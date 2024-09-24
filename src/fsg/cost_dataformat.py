class CostFormData:
    def __init__(
        self,
        type=None,
        subtype=None,
        subtype_name=None,
        comments="TODO",
        quantity=1,
        costs=0.0,
        comments_costs="TODO",
    ):
        """
        Initializes an instance of the CostFormData class with the provided parameters.

        Parameters:
            type (str): The type field, e.g.,  'Material', 'Process', 'Fastener', 'Tooling'.
            subtype (str): The subtype of the item, e.g., '2-component adhesive', 'Carbon Fiber, 1 Ply', etc.
            subtype_name (str, optional): Optional field for the subtype name if the default options don't apply.
            comments (str, optional): Comments related to the item.
            quantity (int): The quantity of the item.
            costs (float): The cost per piece of the item.
            comments_costs (str, optional): Optional comments related to costs.
        """
        self.type: str = type
        self.subtype: str = subtype
        self.subtype_name: str = subtype_name
        self.comments: str = comments
        self.quantity: int = quantity
        self.costs: float = costs
        self.comments_costs: str = comments_costs

    def __repr__(self):
        """
        Provide a string representation of the CostFormData object.

        Returns:
            str: A string that includes the type, subtype, subtype_name, comments,
                 quantity, costs, comments_costs, and sorting attributes of the object.
        """
        return (
            f"CostFormData(type={self.type}, subtype={self.subtype}, subtype_name={self.subtype_name}, "
            f"comments={self.comments}, quantity={self.quantity}, costs={self.costs}, "
            f"comments_costs={self.comments_costs})"
        )
