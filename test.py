import lib

t = True
f = False
u = lib.unit(('one',t,t),('two',t,t),('five',f,f))
d=lib.Db()

d.init_db()
d.create_user(1, u)
d.create_user(2, u)
d.change_diff(2, 3)
u2 = lib.unit(('hello', t,t),('google',t,t),('seven',f,f))
d.create_user(1, u2)
d.add_unit(1, u2)

print(d.get_lesson(1))
print(d.get_lesson(2))
print(d.get_recomendation(2, 1, 0.1))