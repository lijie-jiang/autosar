"""Unit tests for unit elements."""

# pylint: disable=missing-class-docstring, missing-function-docstring
import uuid
import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import autosar.xml.element as ar_element # noqa E402
import autosar # noqa E402


class TestPhysicalDimensionRef(unittest.TestCase):
    def test_write_read_default(self):
        element = ar_element.PhysicalDimensionRef("/PhysDimensions/Dimension")
        writer = autosar.xml.Writer()
        xml = '<PHYSICAL-DIMENSION-REF DEST="PHYSICAL-DIMENSION">/PhysDimensions/Dimension</PHYSICAL-DIMENSION-REF>'
        self.assertEqual(writer.write_str_elem(element), xml)
        reader = autosar.xml.Reader()
        elem: ar_element.PhysicalDimensionRef = reader.read_str_elem(xml)
        self.assertIsInstance(elem, ar_element.PhysicalDimensionRef)
        self.assertEqual(str(elem), "/PhysDimensions/Dimension")

class TestUnit(unittest.TestCase): # noqa D101

    def test_write_read_short_name_only(self): # noqa D102
        test_uuid = uuid.uuid4()
        element = ar_element.Unit(name="MyUnit", uuid_str=str(test_uuid))
        writer = autosar.xml.Writer()
        xml = f'''<UNIT UUID="{test_uuid}">
  <SHORT-NAME>MyUnit</SHORT-NAME>
</UNIT>'''
        print(writer.write_str_elem(element))
        self.assertEqual(writer.write_str_elem(element), xml)
        reader = autosar.xml.Reader()
        elem: ar_element.Unit = reader.read_str_elem(xml)
        self.assertIsInstance(elem, ar_element.Unit)
        self.assertEqual(elem.name, "MyUnit")

    def test_write_read_display_name(self): # noqa D102
        test_uuid = uuid.uuid4()
        element = ar_element.Unit(name="MyUnit", display_name="MyUnit", uuid_str=str(test_uuid))
        writer = autosar.xml.Writer()
        xml = f'''<UNIT UUID="{test_uuid}">
  <SHORT-NAME>MyUnit</SHORT-NAME>
  <DISPLAY-NAME>MyUnit</DISPLAY-NAME>
</UNIT>'''
        self.assertEqual(writer.write_str_elem(element), xml)
        reader = autosar.xml.Reader()
        elem: ar_element.Unit = reader.read_str_elem(xml)
        self.assertIsInstance(elem, ar_element.Unit)
        self.assertIsInstance(elem.display_name, ar_element.SingleLanguageUnitNames)
        self.assertEqual(str(elem.display_name), "MyUnit")

    def test_write_read_factor(self): # noqa D102
        test_uuid = uuid.uuid4()
        element = ar_element.Unit("MyUnit", factor=0.1, uuid_str=str(test_uuid))
        writer = autosar.xml.Writer()
        xml = f'''<UNIT UUID="{test_uuid}">
  <SHORT-NAME>MyUnit</SHORT-NAME>
  <FACTOR-SI-TO-UNIT>0.1</FACTOR-SI-TO-UNIT>
</UNIT>'''
        self.assertEqual(writer.write_str_elem(element), xml)
        reader = autosar.xml.Reader()
        elem: ar_element.Unit = reader.read_str_elem(xml)
        self.assertIsInstance(elem, ar_element.Unit)
        self.assertEqual(elem.factor, 0.1)

    def test_write_read_offset(self): # noqa D102
        test_uuid = uuid.uuid4()
        element = ar_element.Unit("MyUnit", offset=-140.0, uuid_str=str(test_uuid))
        writer = autosar.xml.Writer()
        xml = f'''<UNIT UUID="{test_uuid}">
  <SHORT-NAME>MyUnit</SHORT-NAME>
  <OFFSET-SI-TO-UNIT>-140</OFFSET-SI-TO-UNIT>
</UNIT>'''
        self.assertEqual(writer.write_str_elem(element), xml)
        reader = autosar.xml.Reader()
        elem: ar_element.Unit = reader.read_str_elem(xml)
        self.assertIsInstance(elem, ar_element.Unit)
        self.assertEqual(elem.offset, -140.0)

    def test_write_read_physical_dimension_ref(self): # noqa D102
        test_uuid = uuid.uuid4()
        element = ar_element.Unit("MyUnit", uuid_str=str(test_uuid),
                                  physical_dimension_ref=ar_element.PhysicalDimensionRef("/Dimensions/Dim1"))
        writer = autosar.xml.Writer()
        xml = f'''<UNIT UUID="{test_uuid}">
  <SHORT-NAME>MyUnit</SHORT-NAME>
  <PHYSICAL-DIMENSION-REF DEST="PHYSICAL-DIMENSION">/Dimensions/Dim1</PHYSICAL-DIMENSION-REF>
</UNIT>'''
        self.assertEqual(writer.write_str_elem(element), xml)
        reader = autosar.xml.Reader()
        elem: ar_element.Unit = reader.read_str_elem(xml)
        self.assertIsInstance(elem, ar_element.Unit)
        self.assertEqual(str(elem.physical_dimension_ref), "/Dimensions/Dim1")


if __name__ == '__main__':
    unittest.main()
