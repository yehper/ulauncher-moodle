from requests import post
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RenderResultListAction import \
    RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
import datetime

REST_SERVER = "/webservice/rest/server.php"

def get_events(fname, token, url):
    """
    :param fname: function for request
    :param token: user token
    :return: dictionary/list containing the result of the query
    """
    req_params = {"wstoken": token, 'moodlewsrestformat': 'json',
                  "wsfunction": fname}
    response = post(url + REST_SERVER, req_params)
    response = response.json()
    return response


class MoodleEvents(Extension):
    """
    A class for fetching and displaying moodle upcoming events
    """

    def __init__(self):
        super(MoodleEvents, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        site = extension.preferences['site']
        token = extension.preferences['token']
        data = get_events('core_calendar_get_calendar_upcoming_view',
                          token, site)

        items = []
        for event in data['events']:
            # convert epoch time to readable
            time = datetime.datetime.fromtimestamp(event['timestart']).strftime(
                "%d/%m/%y, %H:%M")
            # TODO handle idn and url better?
            try:
                idn = event['course']['id']
            except:
                idn = ''
            try:
                url = event['url']
            except:
                url = ''
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=f"{idn} - {event['name']}:   {time}",
                                             on_enter=OpenUrlAction(
                                                 url)))

        return RenderResultListAction(items)


if __name__ == '__main__':
    MoodleEvents().run()
