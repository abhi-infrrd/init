import os
import ftplib
import codecs
import pandas as pd
import argparse
import config

# Assumption: FTP Server link to be stored in a text file
ftp_filename = ""


# Filenames are in filename_mmddyy format

# def download_files_from_server(ftp_server_path,local_path):
#     file_list =
#     for files in file_list:
#         ftp = ftplib.FTP("Server IP")
#         ftp.login("UserName", "Password")
#         if os.path.exists(local_path):
#            ftp.cwd(local_path)
#         else:
#             os.mkdir(local_path)
#         ftp.retrbinary("RETR " + files, open(files, 'wb').write)
#         ftp.quit()

def read_user_files_from_local_and_merge(local_path):
    # Read file for User Completion
    doc = codecs.open(config.user_enrollments_completions_file["file_name"], 'rU',
                      config.user_enrollments_completions_file["encoding"])
    user_completion = pd.read_csv(doc, sep='\t')
    user_completion.drop_duplicates(subset=None, keep='first', inplace=True)

    # Read file for User Subscription
    doc = codecs.open(config.user_subscriptions_file["file_name"], 'rU',
                      config.user_subscriptions_file["encoding"])
    user_subscriptions = pd.read_csv(doc, sep='\t')
    user_subscriptions.drop_duplicates(subset=None, keep='first', inplace=True)

    # Read file for user Expertise
    doc = codecs.open(config.user_expertise_file["file_name"], 'rU',
                      config.user_expertise_file["encoding"])
    user_expertise = pd.read_csv(doc, sep='\t')
    user_expertise.drop_duplicates(subset=None, keep='first', inplace=True)

    # Read file for User Interest
    doc = codecs.open(config.user_interest_file["file_name"], 'rU', config.user_interest_file["encoding"])
    user_interest = pd.read_csv(doc, sep='\t')
    user_interest.drop_duplicates(subset=None, keep='first', inplace=True)

    # Read file for User Jurisdictions
    doc = codecs.open(config.user_jurisdictions_file["file_name"], 'rU',
                      config.user_jurisdictions_file["encoding"])
    user_jurisdiction = pd.read_csv(doc, sep='\t')
    user_jurisdiction.drop_duplicates(subset=None, keep='first', inplace=True)

    # Read file for User Credentials
    doc = codecs.open(config.user_credentials_file["file_name"], 'rU', config.user_credentials_file["encoding"])
    user_credentials = pd.read_csv(doc, sep='\t')
    user_credentials.drop_duplicates(subset=None, keep='first', inplace=True)

    # Read file for User Demographics
    doc = codecs.open(config.user_demographics_file["file_name"], 'rU', config.user_demographics_file["encoding"])
    user_demographics = pd.read_csv(doc, sep = '\t')
    user_demographics.drop_duplicates(subset=None, keep='first', inplace=True)
    user_demographics.rename(columns={'UserID':'EncryptedRecordID'}, inplace=True)

    # Finished reading..start merging

    # First merge to create a user vs user demographic file
    user_merged_file = pd.merge(user_interest, user_demographics, how='outer', on=['EncryptedRecordID'])
    user_merged_file['Interest'] = user_merged_file['Interest'].astype(str)
    user_merged_file = user_merged_file.groupby('EncryptedRecordID').agg({'Interest': ', '.join,
                                                                          'PhoneNumber': 'first',
                                                                          'State': 'first',
                                                                          'ZipCode': 'first',
                                                                          'CityStateZip': 'first'
                                                                          }).reset_index()

    user_merged_file = pd.merge(user_merged_file, user_expertise, how='outer', on=['EncryptedRecordID'])
    user_merged_file['Expertise'] = user_merged_file['Expertise'].astype(str)
    user_merged_file = user_merged_file.groupby('EncryptedRecordID').agg({'Expertise': ', '.join,
                                                                          'PhoneNumber': 'first',
                                                                          'State': 'first',
                                                                          'ZipCode': 'first',
                                                                          'CityStateZip': 'first',
                                                                          'Interest': 'first'
                                                                          }).reset_index()

    user_merged_file = pd.merge(user_merged_file, user_credentials, how='outer', on=['EncryptedRecordID'])
    user_merged_file['Credential'] = user_merged_file['Credential'].astype(str)
    user_merged_file = user_merged_file.groupby('EncryptedRecordID').agg({'Credential': ','.join,
                                                                          'Expertise': 'first',
                                                                          'PhoneNumber': 'first',
                                                                          'State': 'first',
                                                                          'ZipCode': 'first',
                                                                          'CityStateZip': 'first',
                                                                          'Interest': 'first'
                                                                          }).reset_index()

    user_merged_file = pd.merge(user_merged_file, user_jurisdiction, how='outer', on=['EncryptedRecordID'])
    user_merged_file['Jurisdiction'] = user_merged_file['Jurisdiction'].astype(str)
    user_merged_file = user_merged_file.groupby('EncryptedRecordID').agg({'Jurisdiction': ','.join,
                                                                          'Credential': 'first',
                                                                          'Expertise': 'first',
                                                                          'PhoneNumber': 'first',
                                                                          'State': 'first',
                                                                          'ZipCode': 'first',
                                                                          'CityStateZip': 'first',
                                                                          'Interest': 'first'
                                                                          }).reset_index()
    # Save merged file to disk
    user_merged_file.to_csv('user_demographics_aggregated.csv', sep='\t', index=False)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_folder', help=" Full path to where the files are stored", required=True)
    args = parser.parse_args()
    if not os.path.exists(args.input_folder):
        os.mkdir(args.input_folder)
    # download_files_from_server(args.input_folder)
    read_user_files_from_local_and_merge(args.input_folder)

