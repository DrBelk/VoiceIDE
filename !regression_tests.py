import os
import WordHandler

TEXT_BASED = 'tests/text_based/'

passed = 0
failed = 0
failed_tests = ''

for test_folder in next(os.walk(TEXT_BASED))[1]:
    wh = WordHandler.WordHandler()
    with open(TEXT_BASED + test_folder + '/input.txt', 'r') as file:
        input_data = file.read().replace('\n', ' ')

        for word in input_data.split():
            wh_output = wh.sendWord(word)

    with open(TEXT_BASED + test_folder + '/output.txt', 'r') as file:
        gold_data = file.read()

        if gold_data == wh_output:
            passed += 1
        else:
            failed += 1
            failed_tests += (test_folder + ', ')

print ('Passed: ' + str(passed) + '/' + str(passed + failed))

failed_tests = failed_tests[:-2] if failed_tests else failed_tests
if failed:
    print ('Failed numbers: ' + failed_tests)

input("Press Enter to close the test results...")
