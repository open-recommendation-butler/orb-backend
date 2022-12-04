from django.shortcuts import render

def search(request):
  context= {
    "articles": [
      {
        "title": "Django’s role in forms",
        "teaser": "Vor einem Jahr, am 8. Dezember 2021, endete die Kanzlerschaft von Angela Merkel. Lange galt sie als umsichtige Krisenkanzlerin,..."
      },
      {
        "title": "Short Message Service: Merkels geliebter Kurznachrichtendienst, die SMS, wird 30",
        "teaser": "Mit Angela Merkel hat die prominenteste Verfasserin von SMS die politische Bühne verlassen. Als Bundeskanzlerin hat sie immer per SMS..."
      },
      {
        "title": "Glosse: Wie Markus Söder in Retzstadt die Merkel-Transformation begonnen hat",
        "teaser": "Dorfladeneröffnung und Weihnachtspostfiliale haben den Ministerpräsidenten nach Main-Spessart gelockt. Unser Autor deutet seinen Auftritt..."
      }
    ]
  }
  return render(request, 'search/results.html', context)