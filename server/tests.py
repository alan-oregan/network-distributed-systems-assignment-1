import command
import utility


# ========= create mock data =========


f = open("./public/test.txt", "w+")
f.write("test123")
f.close()


# ========= utility tests =========


# test parsePath()
expected = (True, "./public/test.txt")
result = utility.parsePath("<SPLIT-test.txt>")

assert result == expected, \
    f"bytes matching {expected} expected, got: {result} instead"


# ========= command tests =========


# test get()
expected = b"test123"
result = command.get("./public/test.txt")

assert result == expected, \
    f"bytes matching {expected} expected, got: {result} instead"


# test split()
expected = "./public/test"
result = command.split("./public/test.txt")

assert result == expected, \
    f"string matching {expected} expected, got: {result} instead"


# test hash()
expected = "ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae"
result = command.hash("./public/test.txt")

assert result == expected, \
    f"string matching {expected} expected, got: {result} instead"


# test list()
expected = "1.txt"
result = command.list("./public/test")

assert result == expected, \
    f"string matching {expected} expected, got: {result} instead"


# test delete()
expected = "./public/test.txt ./public/test/"
result = command.delete("./public/test.txt")

assert result == expected, \
    f"string matching {expected} expected, got: {result} instead"


# ========= end tests =========

print("Success! - Passed all assertions")
