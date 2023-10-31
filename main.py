import zipfile, os, shutil

import pandas as pd

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def generate_csv_file(outputfile, file_list, loss_list, acc_list, pre_list, rec_list, roc_list,
                      epochs_list, lr_list, bs_list, ts_list):
    data = {
        'File': file_list,
        'Epochs': epochs_list,
        'Learning Rate': lr_list,
        'Batch Size': bs_list,
        'Threshold': ts_list,
        'Loss': loss_list,
        'Accuracy': acc_list,
        'Precision': pre_list,
        'Recall': rec_list,
        'ROC': roc_list
    }

    df = pd.DataFrame(data)

    df.to_csv(outputfile, index=False)

    print(f'File CSV created: {outputfile}')


def retrieve_results(zip_file_name, main_directory, storage_directory, loss_list, acc_list, pre_list, rec_list,
                     roc_list, epochs_list, lr_list, bs_list, ts_list):
    zip_file_path = os.path.join(main_directory, zip_file_name)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(storage_directory)

    for file_dir in os.listdir(storage_directory):
        if file_dir.endswith('.txt'):

            file_to_check = os.path.join(storage_directory, file_dir)

            with open(file_to_check, 'r') as file_txt:

                for line in file_txt.readlines():

                    if 'Test' in line:
                        line = line.replace('Test: ', '').replace(' \n', '').replace('[', '').replace(']', '').split(
                            ',')
                        loss_list.append(float(line[0]))
                        acc_list.append(float(line[1]))
                        pre_list.append(float(line[2]))
                        rec_list.append(float(line[3]))
                        roc_list.append(float(line[4]))
                    elif 'Epochs:' in line:

                        line = line.replace('Epochs:', '').replace(' \n', '')
                        epochs_list.append(line)

                    elif 'Batch Size:' in line:

                        line = line.replace('Batch Size:', '').replace(' \n', '')
                        bs_list.append(line)

                    elif 'Learning Rate:' in line:

                        line = line.replace('Learning Rate:', '').replace(' \n', '')
                        lr_list.append(line)

                    elif 'Threshold:' in line:
                        line = line.replace('Threshold:', '').replace(' \n', '')
                        ts_list.append(line)

    shutil.rmtree(storage_directory)


if __name__ == '__main__':

    ans_q = input('Are the zipper files stored in this folder? (Y/N): ')

    if ans_q.lower() == 'y':
        folder_to_store_zip_files = os.path.join(APP_ROOT, 'zip')
    else:
        new_path = input('Insert new path: ')
        folder_to_store_zip_files = os.path.join(APP_ROOT, new_path)

    folder_to_store_unzipped_files = os.path.join(APP_ROOT, 'unzipped')

    epochs = list()
    learning_rate = list()
    batch_size = list()
    threshold = list()

    test_files_name = list()
    test_loss = list()
    test_acc = list()
    test_pre = list()
    test_rec = list()
    test_roc = list()

    if not os.path.exists(folder_to_store_unzipped_files):
        os.mkdir(folder_to_store_unzipped_files)

    if not os.path.exists(folder_to_store_zip_files):
        os.mkdir(folder_to_store_zip_files)

    for file in os.listdir(folder_to_store_zip_files):

        if file.endswith('.zip'):
            test_files_name.append(file)
            print(f'Unzipping: {file}')
            retrieve_results(zip_file_name=file, main_directory=folder_to_store_zip_files,
                             storage_directory=folder_to_store_unzipped_files, loss_list=test_loss, acc_list=test_acc,
                             pre_list=test_pre, rec_list=test_rec, roc_list=test_roc, epochs_list=epochs,
                             bs_list=batch_size, lr_list=learning_rate, ts_list=threshold)

    out = os.path.join(APP_ROOT, 'out.csv')
    generate_csv_file(outputfile=out, file_list=test_files_name, loss_list=test_loss, acc_list=test_acc,
                      pre_list=test_pre, rec_list=test_rec, roc_list=test_roc, epochs_list=epochs, lr_list=learning_rate,
                      ts_list=threshold, bs_list=batch_size)
