# # string concatenation
# # create a string "subscribe to ______"
# youtuber = "Rubén"  # some string

# # a few ways:
# print("subscribe to " + youtuber)
# print("subscribe to {}".format(youtuber))
# print(f"subscribe to {youtuber}")

# with inputs
adj = input("Adjective: ")
verb1 = input("Verb: ")
verb2 = input("Verb: ")
famous_person = input("Famous person: ")

madlib = f"Computer programming is so {adj}! It makes me excited because I love to {verb1}. Stay hydrated and {verb2} like you are {famous_person}!"

print(madlib)
