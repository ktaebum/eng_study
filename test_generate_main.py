from tb_voca import word_test

generator = word_test.TestGenerator('./toefl', section2=True, section3=True)

generator.generate_tests()
