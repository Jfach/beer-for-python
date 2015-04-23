import re

from BeautifulSoup import BeautifulSoup as bs

import beer_data
import bad_beer as errors

class Beer:
    def __init__(self, name):
        try:
            self.name = name.title()

            #keep the raw html, just in case we want it
            self._html = beer_data.beer_profile_html(name)
            self._soup = bs(self._html)
            
            self.score = self.get_score()
            self.score_text = self.get_score_text()
            self.brewer = self.get_brewer()
            self.style = self.get_style()
            self.abv = self.get_abv()

            self.description = self.get_description()
        except errors.Invalid_Beer as error:
            print(error.args[0])
        except AttributeError:
            #This is never reached from this try block, I think?
            print("you are trying to call a data retrieval method"
                  "on a beer that could not be found")

    def __repr__(self):
            return "{}(\"{}\")".format(
                    self.__class__.__name__,
                    self.name)

    def get_abv(self):
        styleabv = self._soup.firstText("Style | ABV")
        text = styleabv.parent.parent.getText()

        abv = re.search(r'([0-9.]+%)ABV', text)

        #what about beers with multiple styles? (TODO)
        #NB: I haven't found an example of that yet
        return abv.groups()[0]

    def get_style(self):
        styleabv = self._soup.firstText("Style | ABV")
        style = styleabv.findNext('b').getText()

        return style

    def get_brewer(self):
        brewed_by_text = self._soup.firstText("Brewed by:")
        brewer = brewed_by_text.findNext('b').getText()

        return brewer

    def get_score(self):
        score = self._soup.find(attrs={"class": "BAscore_big ba-score"})

        return score.getText(), rating_text.getText()

    def get_score_text(self):
        score_text = self._soup.find(attrs={"class": "ba-score_text"})

        return score_text

    def get_description(self):
        #is this ever not "No notes at this time."?
        desc = self._soup.firstText("Notes &amp; Commercial Description:")

        all_text = desc.parent.parent.contents

        #without a page that has something other than "No notes at this time.",
        #it's pretty difficult to know how to handle this section if there's
        #ever more than the one line
        #if beeradvocate.com ever add in descriptions, this will need
        #to be revisited (TODO, I guess)
        return all_text[-1]
