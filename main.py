from xml.dom import minidom
import random
import datetime
from dateutil.relativedelta import relativedelta

# use a set seed to ensure data is consistent
random.seed(1)


class SwimXMLWriter:
    """
    A class for generating xml files for use with the Swim import_xml function.
    """

    def __init__(self):
        """
        Initialize the class with a document and a root element
        """
        self.doc = minidom.Document()
        self.root = self.doc.createElement("data")
        self.doc.appendChild(self.root)

    def create_indicator(self, name, type_, class_type):
        """
        Create an indicator element and add it to the root element.
        :param name: str, the name of the indicator.
        :param type_: str, the type of the indicator.
        :param class_type: str, the class of the indicator.
        """
        indicator = self.doc.createElement("indicator")
        indicator.setAttribute("name", name)
        indicator.setAttribute("type", type_)
        indicator.setAttribute("class", class_type)
        self.root.appendChild(indicator)

    def create_indicator_category(self, name, class_type, indicators=[]):
        """
        Create an indicatorcategory element and add it to the root element.
        :param name: str, the name of the indicator category.
        :param class_type: str, the class of the indicator category.
        :param indicators: list, a list of indicator names to map to this category.
        """
        indicator_category = self.doc.createElement("indicatorcategory")
        indicator_category.setAttribute("name", name)
        indicator_category.setAttribute("class", class_type)
        for indicator in indicators:
            map_ = self.doc.createElement("map")
            map_.setAttribute("indicator", indicator)
            indicator_category.appendChild(map_)
        self.root.appendChild(indicator_category)

    def create_site(
        self, name, site_type, categories=[], parent="", start_date="", end_date=""
    ):
        """
        Create a site element and add it to the root element.
        :param name: str, the name of the site.
        :param type_: str, the type of the site.
        :param categories: list, a list of categories to map to this site.
        :param parent: str, the parent site of this site.
        :param start_date: str, the start date of the site in the format 'YYYY-MM-DD'.
        :param end_date: str, the end date of the site in the format 'YYYY-MM-DD'.
        """
        site = self.doc.createElement("site")
        site.setAttribute("name", name)
        site.setAttribute("type", site_type)
        if parent:
            site.setAttribute("parent", parent)
        if start_date:
            site.setAttribute("start_date", start_date)
        if end_date:
            site.setAttribute("end_date", end_date)
        for category in categories:
            map_ = self.doc.createElement("map")
            map_.setAttribute("category", category)
            site.appendChild(map_)
        self.root.appendChild(site)

    def create_access_group(self, name, users=[], sites={}):
        """
        Create an accessgroup element and add it to the root element.
        :param name: str, the name of the access group.
        :param users: list, a list of user names to add to this group.
        :param sites: dict, a dictionary containing site names as keys and lists of category names as values.
        """
        access_group = self.doc.createElement("accessgroup")
        access_group.setAttribute("name", name)
        for user in users:
            user_el = self.doc.createElement("user")
            user_el.setAttribute("name", user)
            access_group.appendChild(user_el)
        for site, categories in sites.items():
            site_el = self.doc.createElement("site")
            site_el.setAttribute("name", site)
            for category in categories:
                category_el = self.doc.createElement("category")
                category_el.setAttribute("name", category)
                site_el.appendChild(category_el)
            access_group.appendChild(site_el)
        self.root.appendChild(access_group)

    def create_ops_data(
        self,
        site,
        indicator,
        num_records,
        values=[],
        dynamic_date=None,
        from_date=None,
        step_years=0,
        step_months=0,
        step_days=0,
        step_hours=0,
    ):
        """
        Create 'num_records' number of 'data' elements and add it to 'operationsdata' element.
        :param site: str, the name of the site the data belongs to.
        :param indicator: str, the name of the indicator the data belongs to.
        :param num_records: int, the number of data records to be created.
        :param values: list, a list of possible values that can be assigned to each data element.
        :param dynamic_date: str, a string that represents the relative time period. eg: '-12 months'
        :param from_date: str, the starting date for the data records. Format: 'YYYY-MM-DD'
        :param step_years: int, the number of years to step forward for each record.
        :param step_months: int, the number of months to step forward for each record.
        :param step_days: int, the number of days to step forward for each record.
        :param step_hours: int, the number of hours to step forward for each record.
        """
        ops_data = self.doc.createElement("operationsdata")
        ops_data.setAttribute("site", site)
        ops_data.setAttribute("indicator", indicator)
        if dynamic_date is None:
            date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
            for i in range(num_records):
                value = random.choice(values)
                data = self.doc.createElement("data")
                data.setAttribute("date", date.strftime("%Y-%m-%d %H:%M:%S"))
                data.setAttribute("value", value)
                ops_data.appendChild(data)
                date += relativedelta(
                    years=step_years,
                    months=step_months,
                    days=step_days,
                    hours=step_hours,
                )
        else:
            current_date = datetime.datetime.now()
            for i in range(num_records):
                value = random.choice(values)
                data = self.doc.createElement("data")
                data.setAttribute("dynamic_date", dynamic_date)
                data.setAttribute("value", value)
                ops_data.appendChild(data)
                dynamic_date = (current_date + relativedelta(months=+1)).strftime(
                    "- %m months"
                )
        self.root.appendChild(ops_data)

    def save_xml(self, file_path):
        with open(file_path, "w") as f:
            f.write(self.doc.toprettyxml())

    def create_multiple_indicators(self, indicators):
        """
        Add multiple indicators at once.
        :param indicators: list, a list of dictionaries containing the name, ind_type, and class of each indicator.
        """

        for indicator in indicators:
            self.create_indicator(
                indicator["name"], indicator["ind_type"], indicator["class_type"]
            )

    def create_multiple_categories(self, categories):
        """
        Add multiple indicator categories at once.
        :param categories: list, a list of dictionaries containing the name, cat_class, and indicators of each category.
        """
        for category in categories:
            self.create_indicator_category(
                category["name"], category["cat_class"], category["indicators"]
            )

    def create_multiple_sites(self, sites):
        """
        Add multiple sites at once.
        :param sites: list, a list of dictionaries containing the name, type, categories, parent, start_date, and end_date of each site.
        """
        for site in sites:
            self.create_site(**site)

    def create_multiple_access_groups(self, groups):
        """
        Add multiple access groups at once.
        :param groups: list, a list of dictionaries containing the name, users, and sites of each group.
        """
        for group in groups:
            self.create_access_group(**group)

    def create_multiple_ops_data(self, data_list):
        """
        Create multiple operations data elements and add them to the root element.
        :param data_list: list of dict, each dict contains the following keyword arguments:
        site: str, the name of the site.
        indicator: str, the name of the indicator.
        num_records: int, the number of records to create.
        values: list of str, the values of the records.
        dynamic_date: None or str, the dynamic date of the records.
        from_date: str, the starting date of the records in the format 'YYYY-MM-DD'
        step_years: int, the number of years to step the date.
        step_months: int, the number of months to step the date.
        step_days: int, the number of days to step the date.
        step_hours: int, the number of hours to step the date.
        """
        for data in data_list:
            self.create_ops_data(**data)


if __name__ == "__main__":
    writer = SwimXMLWriter()

    indicator_list = [
        {"name": "ecoli", "class_type": "T", "ind_type": "2"},
        {"name": "e coli", "class_type": "N", "ind_type": "2"},
        {"name": "e.coli", "class_type": "T", "ind_type": "2"},
        {"name": "coliforms", "class_type": "N", "ind_type": "2"},
        {"name": "potato", "class_type": "N", "ind_type": "2"},
        {"name": "pecolint", "class_type": "N", "ind_type": "2"},
        {"name": "Eschericia coli", "class_type": "T", "ind_type": "2"},
    ]
    writer.create_multiple_indicators(indicator_list)

    indicator_category_list = [
        {
            "name": "cat1",
            "cat_class": "3",
            "indicators": ["ecoli", "e coli", "coliforms"],
        },
        {"name": "cat2", "cat_class": "3", "indicators": ["potato", "e.coli"]},
        {"name": "cat3", "cat_class": "3", "indicators": ["pecolint"]},
        {"name": "cat4", "cat_class": "3", "indicators": ["Eschericia coli"]},
    ]

    writer.create_multiple_categories(indicator_category_list)

    site_list = [
        {"name": "scheme1", "site_type": "6", "categories": []},
        {"name": "scheme2", "site_type": "6", "categories": []},
        {
            "name": "scheme3",
            "site_type": "6",
            "categories": [],
            "start_date": "1990-12-12",
            "end_date": "2021-12-12",
            "parent":""
        },
        {
            "name": "site1",
            "site_type": "5",
            "categories": ["cat1", "cat2"],
            "parent": "scheme1",
        },
        {
            "name": "site2",
            "site_type": "5",
            "categories": ["cat2"],
            "parent": "scheme2",
        },
        {
            "name": "site1_child1",
            "site_type": "5",
            "categories": ["cat3"],
            "parent": "site1",
        },
        {
            "name": "site4",
            "site_type": "5",
            "categories": ["cat4"],
            "parent": "scheme3",
        },
    ]
    writer.create_multiple_sites(site_list)

    access_group_list = [
        {
            "name": "group1",
            "users": ["admin"],
            "sites": {
                "scheme1": [],
                "scheme2": [],
                "scheme3": [],
                "site1": ["cat1", "cat2"],
                "site2": ["cat2"],
                "site1_child1": ["cat3"],
                "site4": ["cat4"],
            },
        }
    ]
    writer.create_multiple_access_groups(access_group_list)

    data_list = [
        {
            "site": "site1",
            "indicator": "ecoli",
            "num_records": 100,
            "values": ["valid", "invalid"],
            "from_date": "2022-01-01",
            "step_years": 0,
            "step_months": 1,
            "step_days": 1,
            "step_hours": 2,
        },
        {
            "site": "site1",
            "indicator": "e coli",
            "num_records": 100,
            "values": ["&lt;1", "0", "0.1", "&lt;10"],
            "from_date": "2022-01-01",
            "step_years": 0,
            "step_months": 0,
            "step_days": 7,
            "step_hours": 2,
        },
        {
            "site": "site2",
            "indicator": "e.coli",
            "num_records": 50,
            "values": ["valid", "invalid", "pass", "fail", "absent", "present"],
            "from_date": "2021-01-01",
            "step_years": 0,
            "step_months": 0,
            "step_days": 9,
            "step_hours": 2,
        },
        {
            "site": "site1_child1",
            "indicator": "pecolint",
            "num_records": 50,
            "values": ["1", "2", "&lt;1"],
            "from_date": "2022-01-01",
            "dynamic_date": None,
            "step_years": 0,
            "step_months": 0,
            "step_days": 10,
            "step_hours": 2,
        },
        {
            "site": "site4",
            "indicator": "ecoli",
            "num_records": 50,
            "values": ["valid", "invalid", "pass", "fail", "absent", "present"],
            "from_date": "2021-01-01",
            "step_years": 0,
            "step_months": 0,
            "step_days": 9,
            "step_hours": 2,
        },
    ]
    writer.create_multiple_ops_data(data_list)

    writer.save_xml("./test.xml")
