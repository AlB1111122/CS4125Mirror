from abc import ABC

class IDataCleaner(ABC):
    def clean(self, data):
        pass

class CSVDataCleaner(IDataCleaner):
    """Class to handle the various forms of cleaning the data"""

    def clean_data(self, data):
        """Clean the data of noise using regex to make it more uniform"""
        noise = r"(sv\s*:)|(wg\s*:)|(ynt\s*:)|(fw(d)?\s*:)|(r\s*:)|(re\s*:)|(\[|\])|(aspiegel support issue submit)|(null)|(nan)|((bonus place my )?support.pt 自动回复:)"
        data["ts"] = (
            data["Ticket Summary"].str
            .lower()
            .replace(noise, " ", regex=True)
            .replace(r'\s+', ' ', regex=True).str
            .strip()
        )
        # temp_debug = data.loc[:, ["Ticket Summary", "ts", "y"]]

        data["ic"] = data["Interaction content"].str.lower()
        noise_1 = [
            r"(from :)|(subject :)|(sent :)|(r\s*:)|(re\s*:)",
            r"(january|february|march|april|may|june|july|august|september|october|november|december)",
            r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)",
            r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
            r"\d{2}(:|.)\d{2}",
            r"(xxxxx@xxxx\.com)|(\*{5}\([a-z]+\))",
            r"dear ((customer)|(user))",
            r"dear",
            r"(hello)|(hallo)|(hi )|(hi there)",
            r"good morning",
            r"thank you for your patience ((during (our)? investigation)|(and cooperation))?",
            r"thank you for contacting us",
            r"thank you for your availability",
            r"thank you for providing us this information",
            r"thank you for contacting",
            r"thank you for reaching us (back)?",
            r"thank you for patience",
            r"thank you for (your)? reply",
            r"thank you for (your)? response",
            r"thank you for (your)? cooperation",
            r"thank you for providing us with more information",
            r"thank you very kindly",
            r"thank you( very much)?",
            r"i would like to follow up on the case you raised on the date",
            r"i will do my very best to assist you"
            r"in order to give you the best solution",
            r"could you please clarify your request with following information:"
            r"in this matter",
            r"we hope you(( are)|('re)) doing ((fine)|(well))",
            r"i would like to follow up on the case you raised on",
            r"we apologize for the inconvenience",
            r"sent from my huawei (cell )?phone",
            r"original message",
            r"customer support team",
            r"(aspiegel )?se is a company incorporated under the laws of ireland with its headquarters in dublin, ireland.",
            r"(aspiegel )?se is the provider of huawei mobile services to huawei and honor device owners in",
            r"canada, australia, new zealand and other countries",
            r"\d+",
            r"[^0-9a-zA-Z]+",
            r"(\s|^).(\s|$)"
        ]
        for noise in noise_1:
            print(noise)
            data["ic"] = data["ic"].replace(noise, " ", regex=True)
        data["ic"] = data["ic"].replace(r'\s+', ' ', regex=True).str.strip()
        # temp_debug = data.loc[:, ["Interaction content", "ic", "y"]]

        print(data.y1.value_counts())
        good_y1 = data.y1.value_counts()[data.y1.value_counts() > 10].index
        data = data.loc[data.y1.isin(good_y1)]
        print(data.shape)
        return data