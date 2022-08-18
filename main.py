from collector import get_data


def main():
    df = get_data("data scientist", 5, False, "C:/Users/Computador/Desktop/Projetos/Python/old_data_sci_project/chromedriver.exe", 1)
    df.to_csv("jobs.csv")

if __name__ == "__main__":
    main()