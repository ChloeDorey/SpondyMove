import smooth
import analysis_figure
import procedures
import analysis001
import analysis002
import analysis003
import analysis004
import analysis005
import analysis006
import analysis007
import analysis008
import analysis009
import Boxplots
import correcteur


def main():
    # analysis001.analysis()
    # analysis002.analysis()
    # analysis003.analysis()
    # analysis004.analysis()
    # analysis005.analysis()
    # analysis006.analysis()
    # analysis007.analysis()
    # analysis008.analysis()
    # analysis009.analysis()
    # analysis_figure.analysis()
    # smooth.analysis()
    # Boxplots.analysis(show=True)

    # Lance toutes les coupures de tout le monde d'un coup
    # procedures.cut_excel_files()
    # smooth.smoothness()

    correcteur.correction()

    # Si on veut effectuer l'analyse avec la creation de figure avec X personne. Ne pas oublier la virgule à la fin de la liste !!
    #analysis_figure.analysis(manual_test=["011_YaJu","019_GuAl",])

main()
