from openpyxl import load_workbook
import pandas as pd
import stable_match
import sys

def next_settings(settings):
    for i in range(group_size):
        if settings[-i - 1] == 0:
            settings[-i - 1] += 1
            return settings
        else:
            settings[-i - 1] = 0
    if settings[0] != 2:
        settings[0] += 1
        return settings
    else:
        return "Complete"


def create_DB():
    settings = [0, 0, 0, 0, 0]
    df_db = pd.DataFrame()
    for i in range(sample_size):
        df_db = df_db.append([settings + stable_match.stable_match(settings)], ignore_index=True)
    while (next_settings(settings)) != "Complete":
        for i in range(sample_size):
            df_db = df_db.append([settings + stable_match.stable_match(settings)], ignore_index=True)
    df_db = df_db.rename(columns={0: "Pursuer", 1: "Pursues left?", 2: "Couple are pursued?",
                                  3: "Influencer / Dominant was already the Pursued?", 4: "Fair pursue?",
                                  5: "Men's dissatisfaction", 6: "Women's dissatisfaction", 7: "Dog's dissatisfaction",
                                  8: "# of iterations"})
    df_db.to_excel("examples\Database_"+str(sample_size)+"_"+str(group_size)+".xlsx", sheet_name="Database")


def calculate_means():
    df_db = pd.read_excel("examples\Database_"+str(sample_size)+"_"+str(group_size)+".xlsx")
    df_means = df_db.groupby(
        ["Pursuer", "Pursues left?", "Couple are pursued?", "Influencer / Dominant was already the Pursued?",
         "Fair pursue?"]).mean()
    df_standard_deviation = df_db.groupby(
        ["Pursuer", "Pursues left?", "Couple are pursued?", "Influencer / Dominant was already the Pursued?",
         "Fair pursue?"]).std()

    writer = pd.ExcelWriter(r"examples\Means&Std_"+str(sample_size)+"_"+str(group_size)+".xlsx", engine='openpyxl')
    df_means.to_excel("examples\Means&Std_"+str(sample_size)+"_"+str(group_size)+".xlsx", sheet_name='Means')
    writer.book = load_workbook(r"examples\Means&Std_"+str(sample_size)+"_"+str(group_size)+".xlsx")
    df_standard_deviation.to_excel(writer, sheet_name='Std', index=False)
    writer.save()
    writer.close()


sample_size=int(sys.argv[1])
group_size=int(sys.argv[2])
create_DB()
calculate_means()