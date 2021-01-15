
phones = ["Apple", "Huawei", "Xiaomi"]

for index, phone in enumerate(phones):
    print("{} phone is {}".format(index, phone))

old_student_score_info = {
    "Jack": {
        "chinese": 87,
        "math": 92,
        "english": 78
    },
    "Tom": {
        "chinese": 92,
        "math": 100,
        "english": 89
    }
}

new_student_score_info = {
    name:scores for name, scores in old_student_score_info.items() if scores['math']== 100
}
print(new_student_score_info)
