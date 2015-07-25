#!/usr/bin/env python

"""This programs defines a class to do an ETL on the City of Torontos'
budgets per ward, from the Excel spreadsheet with these budgets from the Open
Data site of Toronto:

 http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=1dc340271f8e3310VgnVCM1000003dd60f89RCRD

and then plots these budgets on a map of Toronto with the wards, coloring
each ward according to its budget
"""

import re
import xlrd


class TorontoBudgetForecastPerCityWard(object):

    """A class to contain the budget of the City of Toronto per ward.

    Methods:

       constructor: no parameters (initializes internal fields)

       self.etl_excel_spreadsheet(excel_spreadsh_fname)
                does an ETL on the Excel-spreadsheet-filename passed as
                parameter, which is supposed to be the Excel downloaded from
                the Open Data site of the City of Toronto:

                   http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=1dc340271f8e3310VgnVCM1000003dd60f89RCRD

    Fields:

       _budget: a dictionary indexed by [budget_year][ward_number], whose
                value is the float with budget for that year and that ward

       _total_budget_per_ward: a dictionary indexed by [ward_number], whose
                               value is the float with budget for that ward
                               for the next 10 years

       _re_total_ward: a compiled regular-expression to match which rows
                       in the Excel spreadsheet define Total of Budgets per
                       ward.
    """

    def __init__(self):

        # This is budget per ward and per year
        self._budget = dict()
        for year in range(2015, 2026):
            self._budget[year] = dict()

        # total budget in the 10 years span 2015-2025 per ward
        self._total_budget_per_ward = dict()

        # This is the reg-expr pattern which gives us a budget total per ward
        ptt_tot_ward = '(?P<ward_name>.*)-(?P<ward_number>[0-9][0-9]*) Total$'
        self._re_total_ward = re.compile(ptt_tot_ward, re.UNICODE)

    def _save_budgets_of_a_ward(self, excel_budget_row, ward_number):
        """This Excel row 'excel_budget_row' seems to be very likely the row
        with the budgets for each of the next ten years for ward 'ward_number'
        in the City of Toronto.
        Finally check that it is so, and loads that budget into the internal
        data-structures of this instance.
        """

        max_col_numb = len(excel_budget_row) - 1

        # the columns 3 to max_col_numb-1 are the budgets for that ward for
        # years 2015 and so on; e.g., column 3 -> budget 2015,
        # column 4 -> budget 2016, that there is a subtotal column for the
        # first 5 years in column 9th (8th 0-based), so this subtotal-column
        # for 5 years had to be skipped

        range_columns = range(3, 3+5)             # the budgets for 2015..19
        range_columns += range(3+5+1, max_col_numb)  # the remainings 2020...

        current_budget_year = 2015   # this is the year of the first budget
        accum_budget_per_ward = 0.0
        for col_idx in range_columns:  # Iterate through the columns (budgets)
            cell_obj = excel_budget_row[col_idx]
            if cell_obj and cell_obj.ctype == xlrd.XL_CELL_NUMBER:
                ward_budget = float(cell_obj.value)
            else:
                ward_budget = 0.0
            self._budget[current_budget_year][ward_number] = ward_budget
            accum_budget_per_ward += ward_budget
            current_budget_year += 1  # go to the next column (year)

        # this is the total budget of the ward in the 10 years span: the
        # last column of this row (columns are 0-indexed, so the last
        # column is 'max_col_numb-1')
        total_ward_budget = 0.0
        total_of_ward = excel_budget_row[max_col_numb]
        if total_of_ward and total_of_ward.ctype == xlrd.XL_CELL_NUMBER:
            total_ward_budget = float(total_of_ward.value)

        # but we had also accumulated this total in the 10-years-span by
        # adding it above in the for-loop, year by year in this time span,
        # so validate this ETL too
        if total_ward_budget != accum_budget_per_ward:
            print "Something strange in 10-years Total for this Ward %d: Explicit Total and Calculated Total don't agree: %f %f (%f)" % \
                  (ward_number, total_ward_budget, accum_budget_per_ward,
                   (total_ward_budget - accum_budget_per_ward))
            return  # ignore this seemingly Ward Total row

        self._total_budget_per_ward[ward_number] = accum_budget_per_ward

    def _etl_excel_row(self, excel_budget_row):
        """Do an ETL of this row 'excel_budget_row', to see if it is a
        row with the summary 'Total' budget for a city ward for each of the
        next 10 years (there are other rows with budgets per individual
        projects in a ward: we're interested only in the rows which give
        'Total' of budget for a ward for the next 10 years).
        """

        try:
            # Get the col #0 of the Excel row (with description)
            col_0_value = excel_budget_row[0]  # Get the col #0
            # 'ctype == xlrd.XL_CELL_TEXT' means the value is a string
            if not col_0_value or col_0_value.ctype != xlrd.XL_CELL_TEXT:
                return    # ignore this row in the Excel spreadsheet

            # we know now that 'ctype == xlrd.XL_CELL_TEXT', so its value
            # is a Unicode string
            # print type(col_0_value.value), col_0_value.value
            match = self._re_total_ward.match(col_0_value.value)
            if not match:
                return   # no match: this row is not a total per ward
            # It matched: get the ward name and the ward number
            ward_name = match.group('ward_name')
            ward_number = int(match.group('ward_number'))
        except Exception as an_exc:
            print "Exception type is: %s\n" % an_exc
            return  # ignore this row in the Excel spreadsheet

        # The columns 1 and 2 are the Project and Sub-project Names:
        # validate in the ETL that these two columns should have empty
        # values in the case that the row is a total-budget per ward
        col_1_value = excel_budget_row[1]  # Get the col #1
        col_2_value = excel_budget_row[2]  # Get the col #2
        if not col_1_value or not col_2_value:
            return

        if col_1_value.ctype != xlrd.XL_CELL_EMPTY or \
           col_2_value.ctype != xlrd.XL_CELL_EMPTY:
            print "Something strange in Totals for this Ward %s %s:" + \
                  " it has Project or Sub-project Names %s %s:" % \
                   (ward_number, ward_name, col_1_value.value,
                    col_2_value.value)
            return  # ignore this seemingly Ward Total row

        print "Processing budget totals for Ward %d %s" % \
              (ward_number, ward_name)

        self._save_budgets_of_a_ward(excel_budget_row, ward_number)

    def etl_excel_spreadsheet(self, excel_spreadsh_fname):
        """Do an ETL on the Excel spreadsheet 'excel_spreadsh_fname'
        with the budgets of the City of Toronto per Ward for the next
        10 years. This Excel spreadsheet is supposed to have been
        downloaded from:

           http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=1dc340271f8e3310VgnVCM1000003dd60f89RCRD
        """

        # Open the Excel workbook given
        xl_workbook = xlrd.open_workbook(excel_spreadsh_fname)

        # Open the first spreadsheet in this Excel workbook
        xl_sheet = xl_workbook.sheet_by_index(0)

        # Do the ETL for each of the rows in this Excel spreadsheet
        for curr_row_numb in range(0, xl_sheet.nrows):
            self._etl_excel_row(xl_sheet.row(curr_row_numb))

        xl_workbook.release_resources()

        print self._budget
        print self._total_budget_per_ward

    def plot_budget(self):
        """Plot the budget for the next years per ward in the City of
        Toronto, according to the ETL done by the previous method
        etl_excel_spreadsheet() that should have been called already
        """
        # TODO: pending implementation of this method using matplotlib/basemap
        pass


def main():
    """Main function on the program.
    """

    opendata_excel_spreadsh = 'shp_dir/budget_per_city_ward.xlsx'

    toronto_budg_per_neighb = TorontoBudgetForecastPerCityWard()

    # Do the ETL from the Excel spreadsheet first
    toronto_budg_per_neighb.etl_excel_spreadsheet(opendata_excel_spreadsh)

    # Plot the budget using matplotlib/basemap
    toronto_budg_per_neighb.plot_budget()


if __name__ == '__main__':
    main()
