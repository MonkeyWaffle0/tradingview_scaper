import csv


data_id = input("What is the data id ?\n")
rate = input("What prediction rate do you want to apply ?\n")

dataset = "data_training_" + data_id + ".csv"

with open(dataset, "r") as read_file:
    read = csv.reader(read_file)
    data = [item for item in read]
    new_column = []

    for i, line in enumerate(data):
        sum = 0
        try:
            for j in range(1, int(rate) + 1):
                price = float(data[i + j][0])
                sum += price

            average = sum / int(rate)
            new_column.append(average)

        except IndexError:
            pass

    for i, line in enumerate(data):
        try:
            line.append(new_column[i])
        except IndexError:
            pass

new_dataset = "data_test_" + data_id + "_rate" + rate + ".csv"
row = ["price", "ema20", "vol", "vol_ema", "dif_sar", "rsi", "predict"]
with open(new_dataset, 'w', newline="") as write_file:
    writer = csv.writer(write_file)
    writer.writerow(row)
    for line in data:
        writer.writerow(line)

