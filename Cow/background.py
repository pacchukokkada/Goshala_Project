from background_task import background


@background(schedule=5)
def notify():
    print("kundre")

notify(repeat=5)





