#module to create synthetic data

from app.synthetic.Generation import Generation
gen=Generation(session_file="D:/Acadamic/Final Year Research/Project/Final_Year_Project/app/data/sessions.csv",window=10)
gen.mapping(percentage=0.2,no_of_lines_anomaly=5000,file_count=10)