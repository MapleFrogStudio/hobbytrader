# https://medium.datadriveninvestor.com/panel-everything-you-need-to-know-9bca61532e12

import panel as pn
pn.extension()

def model(n=5):
    return "⭐"*n


slider = pn.widgets.IntSlider(value=5, start=1, end=5)
interactive_model = pn.bind(model, n=slider)
layout = pn.Column(slider, interactive_model)

pn.template.FastListTemplate(
    site="Panel", title="Example", main=[layout],
).servable()