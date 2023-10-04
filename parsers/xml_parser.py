import xml.etree.ElementTree as xET

from exceptions.emptyInputError import EmptyInputError


class XmlParser:
    def load_xml(self, file_names: list[str], test_names: dict):
        if len(file_names) > 0:
            for file_name in file_names:
                names = []
                xml_name = file_name.split("/")[-1]
                tree = xET.parse(file_name)
                root = tree.getroot()
                for test in root.findall("test"):
                    clazzes = test.find("classes")
                    for clazz in clazzes.findall("class"):
                        name = clazz.get("name")
                        if name not in test_names:
                            names.append(name)

                if xml_name in test_names:
                    test_names[xml_name].extend([name for name in names if name not in test_names[xml_name]])
                else:
                    test_names[xml_name] = names
        else:
            raise EmptyInputError("no files provided to load_xml")
