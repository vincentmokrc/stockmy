from bursamy.convert import PdfConverter
import sys

#LINUX convert


def main():
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))

    #dir_path = "./test"
    print(sys.argv[1])

    if(sys.argv[2] == 'txt'):
        PdfConverter(sys.argv[1]).convert_all_to_text()
    else:
        PdfConverter(sys.argv[1]).covert_all_to_xml()
    #xml = convert_pdf(dir_path,'xml')
    #print(xml)

if __name__ == "__main__":
    main()