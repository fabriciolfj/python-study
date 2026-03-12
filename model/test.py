from model.Person import Person


def test(person):
    print(f"{person.nome}: {person.endereco}")


person  = Person("fabricio", "rua test")
test(person)