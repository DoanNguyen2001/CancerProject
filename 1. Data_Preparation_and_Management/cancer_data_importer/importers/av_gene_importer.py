from .base_importer import BaseImporter
from datetime import datetime
import logging

#GENEID, Pseudonymised gene ID, Character, The format of this field in the Simulacrum is different from the format of GENEID
#TUMOURID, Pseudonymised tumour ID, Integer, The format of this field in the Simulacrum is deliberately different from the format of pseudonymised tumour id for real individuals
#PATIENTID, Pseudonymised patient ID, Integer, The format of this field in the Simulacrum is deliberately different from the format of pseudonymised patient id for real individuals
#GENE_DESC, Gene description, Character
#GENE, Gene code, Number, Number code of gene from genetictest.tsv (underlying table on genetic table in CAS)
#COUNT_TESTS, Count of genetic tests (dd) on this geneid, Number, The number of genetic tests on this gene based on unique genetic test id
#COUNT_RESULTS, Count of genetic test results (dd) on this geneid, Number
#COUNT_DATE, Number of test dates for this gene, Number, The number of test dates for each gene. (more that >1 test for a gene on same day counts as 1)
#ALL_TESTSTATUSES, Outcome of test is the test status. List of all test statuses ordered by date for this geneid, Character
#OVERALL_TS, Overall test status on whether anything abnormal on this gene, Character
#NO_OF_AB_GATS, Number of abnormal genetic aberration types, only counting definitive not borderline results, Number, Count of one for each of the below five genetic aberration types that are abnormal (max count = 5)
#DNASEQ_GAT, Overall test result for the genetic aberration type 'dna sequence', Character
#METHYL_GAT, Overall test result for the genetic aberration type 'methylation', Character
#EXP_GAT, Overall test result for the genetic aberration type 'expression', Character
#COPYNO_GAT, Overall test result for the genetic aberration type 'copyno', Character#
#FUS_TRANS_GAT, Overall test result for the genetic aberration type 'fusion/translocation', Character
#ABNORMAL_GAT, Type of genetic aberration if only one otherwise 'multiple', Character
#NO_OF_SEQ_VARS, Count of sequence variants for this gene, Number, Should only be populated if dnaseq_gat is not null
#ALL_SEQ_VARS, List of all sequence variants for this gene, Character, As above
#SEQ_VAR, Sequence variant for this gene if only one otherwise 'multiple', Character, As above
#DATE_OVERALL_TS, Test date for overall test status, Date, Based on best date for the worst/most conclusive i.e. overall test status
#BEST_DATE_SOURCE_OVERALL, Source of test (i.e molecular or pathology feed), Character, Based on the test with the best date and worst/most conclusive test status (i.e. test with DATE_OVERALL_TS)
#MIN_DATE, First test date for this gene, Date
#MAX_DATE, Last test date for this gene, Date, Many dates can be given for each genetic test. Each gene can have many best test dates. These variables give the earliest and la
#ALL_PRO_IMPS, List of all protein impacts for this gene, Character, Should only be populated if dnaseq_gat is not null
#NO_PRO_IMPS, Count of protein impacts for this gene, Integer, As above
#PRO_IMP, Protein impacts for this gene if only one otherwise 'multiple', Character, As above
#METHODS, The method of test, Character, For the overall test status
#LAB_NAME, Name of laboratory where test was performed, Character, Indicating if molecular or pathology lab; if molecular then name of molecular lab will be given

class AvGeneImporter(BaseImporter):
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS AV_GENE (
            GENEID CHAR(30) primary key,
            TUMOURID INTEGER,
            PATIENTID INTEGER,
            GENE_DESC CHAR(30),
            GENE INTEGER,
            COUNT_TESTS INTEGER,
            COUNT_RESULTS INTEGER,
            COUNT_DATE INTEGER,
            ALL_TESTSTATUSES CHAR(300),
            OVERALL_TS char(150),
            NO_OF_AB_GATS INTEGER,
            DNASEQ_GAT char(150),
            METHYL_GAT char(150),
            EXP_GAT char(150),
            COPYNO_GAT char(150),
            FUS_TRANS_GAT char(150),
            ABNORMAL_GAT char(150),
            NO_OF_SEQ_VARS INTEGER,
            ALL_SEQ_VARS CHAR(150),
            SEQ_VAR CHAR(150),
            DATE_OVERALL_TS DATE,
            BEST_DATE_SOURCE_OVERALL_TS CHAR(150),
            MIN_DATE DATE,
            MAX_DATE DATE,
            ALL_PRO_IMPS CHAR(150),
            NO_PRO_IMPS INTEGER,
            PRO_IMP CHAR(150),
            METHODS CHAR(150),
            LAB_NAME CHAR(150)
                )''')

    def process_row(self, row):
        try:
            integer_fields = ['TUMOURID', 'PATIENTID', 'GENE', 'COUNT_TESTS', 'COUNT_RESULTS',
                              'COUNT_DATE', 'NO_OF_AB_GATS', 'NO_PRO_IMPS']
            for field in integer_fields:
                if row.get(field) == '':
                    row[field] = None
                elif row.get(field):
                    row[field] = int(row[field])

            date_fields = ['DATE_OVERALL_TS', 'MIN_DATE', 'MAX_DATE']

            for date_field in date_fields:
                if row.get(date_field) and row[date_field].strip():
                    try:
                        row[date_field] = datetime.strptime(row[date_field], '%Y-%m-%d').date()
                    except ValueError:
                        row[date_field] = None
                else:
                    row[date_field] = None

            sql = """INSERT INTO AV_GENE (GENEID, TUMOURID, PATIENTID, GENE_DESC, GENE, 
                     COUNT_TESTS, COUNT_RESULTS, COUNT_DATE, ALL_TESTSTATUSES, OVERALL_TS,
                     NO_OF_AB_GATS, DNASEQ_GAT, METHYL_GAT, EXP_GAT, COPYNO_GAT,
                     FUS_TRANS_GAT, ABNORMAL_GAT, NO_OF_SEQ_VARS, ALL_SEQ_VARS, SEQ_VAR,
                     DATE_OVERALL_TS, BEST_DATE_SOURCE_OVERALL_TS, MIN_DATE, MAX_DATE,
                     ALL_PRO_IMPS, NO_PRO_IMPS, PRO_IMP, METHODS, LAB_NAME)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            values = (
                row['GENEID'], row['TUMOURID'], row['PATIENTID'], row['GENE_DESC'],
                row['GENE'], row['COUNT_TESTS'], row['COUNT_RESULTS'], row['COUNT_DATE'],
                row['ALL_TESTSTATUSES'], row['OVERALL_TS'], row['NO_OF_AB_GATS'],
                row.get('DNASEQ_GAT'), row.get('METHYL_GAT'), row.get('EXP_GAT'),
                row.get('COPYNO_GAT'), row.get('FUS_TRANS_GAT'), row.get('ABNORMAL_GAT'),
                row['NO_OF_SEQ_VARS'], row.get('ALL_SEQ_VARS'), row.get('SEQ_VAR'),
                row['DATE_OVERALL_TS'], row.get('BEST_DATE_SOURCE_OVERALL_TS'),
                row['MIN_DATE'], row['MAX_DATE'], row.get('ALL_PRO_IMPS'),
                row.get('NO_PRO_IMPS'), row.get('PRO_IMP'), row.get('METHODS'),
                row.get('LAB_NAME')
            )
            return sql, values


        except KeyError as ke:
            print(f"Missing key in row: {ke}")
            return None

        except Exception as e:
            print(f"Unexpected error in processing row: {e}")
            return None
