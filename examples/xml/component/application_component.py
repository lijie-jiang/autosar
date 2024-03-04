"""
Sender-receiver port interface examples
"""
import os
import autosar
import autosar.xml.element as ar_element
import autosar.xml.enumeration as ar_enum


def create_platform_types(packages: dict[str, ar_element.Package]):
    """
    Creates necessary platform types
    """
    boolean_base_type = ar_element.SwBaseType('boolean', size=8, encoding="BOOLEAN")
    packages["PlatformBaseTypes"].append(boolean_base_type)
    uint8_base_type = ar_element.SwBaseType('uint8', size=8)
    packages["PlatformBaseTypes"].append(uint8_base_type)
    uint16_base_type = ar_element.SwBaseType('uint16', size=16)
    packages["PlatformBaseTypes"].append(uint16_base_type)
    uint32_base_type = ar_element.SwBaseType('uint32', size=32)
    packages["PlatformBaseTypes"].append(uint32_base_type)
    boolean_data_constr = ar_element.DataConstraint.make_internal("boolean_DataConstr", 0, 1)
    packages["PlatformDataConstraints"].append(boolean_data_constr)
    computation = ar_element.Computation.make_value_table(["FALSE", "TRUE"])
    boolean_compu_method = ar_element.CompuMethod(name="boolean_CompuMethod",
                                                  category="TEXTTABLE",
                                                  int_to_phys=computation)
    packages["PlatformCompuMethods"].append(boolean_compu_method)
    sw_data_def_props = ar_element.SwDataDefPropsConditional(base_type_ref=uint8_base_type.ref(),
                                                             data_constraint_ref=boolean_data_constr.ref(),
                                                             compu_method_ref=boolean_compu_method.ref())
    boolean_impl_type = ar_element.ImplementationDataType("boolean",
                                                          category="VALUE",
                                                          sw_data_def_props=sw_data_def_props)
    packages["PlatformImplementationDataTypes"].append(boolean_impl_type)
    sw_data_def_props = ar_element.SwDataDefPropsConditional(base_type_ref=uint8_base_type.ref())
    uint8_impl_type = ar_element.ImplementationDataType("uint8",
                                                        category="VALUE",
                                                        sw_data_def_props=sw_data_def_props)
    packages["PlatformImplementationDataTypes"].append(uint8_impl_type)
    sw_data_def_props = ar_element.SwDataDefPropsConditional(base_type_ref=uint16_base_type.ref())
    uint16_impl_type = ar_element.ImplementationDataType("uint16",
                                                         category="VALUE",
                                                         sw_data_def_props=sw_data_def_props)
    packages["PlatformImplementationDataTypes"].append(uint16_impl_type)
    sw_data_def_props = ar_element.SwDataDefPropsConditional(base_type_ref=uint32_base_type.ref())
    uint32_impl_type = ar_element.ImplementationDataType("uint32",
                                                         category="VALUE",
                                                         sw_data_def_props=sw_data_def_props)
    packages["PlatformImplementationDataTypes"].append(uint32_impl_type)


# def create_implementation_data_types(packages: dict[str, ar_element.Package]):
#     """
#     Creates non-platform implementation data types
#     """
#     sw_data_def_props = ar_element.SwDataDefPropsConditional(base_type_ref="AUTOSAR_Platform/BaseTypes/uint8")
#     inactive_active_t = ar_element.ImplementationDataType("InactiveActive_T",
#                                                           category="VALUE",
#                                                           sw_data_def_props=sw_data_def_props)
#     packages["ImplementationDataTypes"].append(inactive_active_t)


def create_sender_receiver_port_interfaces(packages: dict[str, ar_element.Package]):
    """
    Create sender-receiver port interfaces used in example
    """
    uint16_impl_t = packages["PlatformImplementationDataTypes"].find("uint16")
    port_interface = ar_element.SenderReceiverInterface("VehicleSpeed_I")
    port_interface.create_data_element("VehicleSpeed", type_ref=uint16_impl_t.ref())
    packages["PortInterfaces"].append(port_interface)
    port_interface = ar_element.SenderReceiverInterface("EngineSpeed_I")
    port_interface.create_data_element("EngineSpeed", type_ref=uint16_impl_t.ref())
    packages["PortInterfaces"].append(port_interface)


def create_client_server_interfaces(packages: dict[str, ar_element.Package]):
    """
    Creates client-server interface with one operation
    """
    uint32_impl_type = packages["PlatformImplementationDataTypes"].find("uint32")
    boolean_impl_type = packages["PlatformImplementationDataTypes"].find("boolean")
    interface = ar_element.ClientServerInterface("FreeRunningTimer_I")
    operation = interface.create_operation("GetTime")
    operation.create_out_argument("value", type_ref=uint32_impl_type.ref())
    operation = interface.create_operation("IsTimerElapsed")
    operation.create_in_argument("startTime", type_ref=uint32_impl_type.ref())
    operation.create_in_argument("duration", type_ref=uint32_impl_type.ref())
    operation.create_out_argument("result", type_ref=boolean_impl_type.ref())
    packages["PortInterfaces"].append(interface)


def save_xml_files(workspace: autosar.xml.Workspace):
    """
    Saves workspace as XML documents
    """
    interface_document_path = os.path.abspath(os.path.join(os.path.dirname(
        __file__), 'data', 'portinterfaces.arxml'))
    datatype_document_path = os.path.abspath(os.path.join(os.path.dirname(
        __file__), 'data', 'datatypes.arxml'))
    platform_document_path = os.path.abspath(os.path.join(os.path.dirname(
        __file__), 'data', 'platform.arxml'))
    workspace.create_document(interface_document_path, packages="/PortInterfaces")
    workspace.create_document(datatype_document_path, packages="/DataTypes")
    workspace.create_document(platform_document_path, packages="/AUTOSAR_Platform")
    workspace.write_documents()


def main():
    """
    Main
    """
    workspace = autosar.xml.Workspace()
    packages = dict(zip(["PlatformBaseTypes",
                         "PlatformImplementationDataTypes",
                         "PlatformDataConstraints",
                         "PlatformCompuMethods",
                         "ImplementationDataTypes",
                         "PortInterfaces"],
                    workspace.make_packages("AUTOSAR_Platform/BaseTypes",
                                            "AUTOSAR_Platform/ImplementationDataTypes",
                                            "AUTOSAR_Platform/DataConstraints",
                                            "AUTOSAR_Platform/CompuMethods",
                                            "DataTypes/ImplementationDataTypes",
                                            "PortInterfaces")))
    create_platform_types(packages)
    create_sender_receiver_port_interfaces(packages)
    create_client_server_interfaces(packages)
    save_xml_files(workspace)


if __name__ == "__main__":
    main()