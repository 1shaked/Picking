import { useAtomValue, useSetAtom } from "jotai";
import { FabiosGenericTable } from "../../../Table/FabiosGenericTable";
import { ParentMealNameAtom, RecipeObjectSchemaForDisplayAtom, SelectedParentMealsAtom, SelectedSourcesAtom, SourceTypeAtom, taskManagementGetDatesListRangeAtom, taskManagementGroupedAtom, taskManagementSelectedItemAtom } from "../state";
import { useMemo, useState } from "react";
import { ColumnDef, ExpandedState, SortingState } from "@tanstack/react-table";
import { TaskManagementGroupedItemType } from "../types/TaskManagementTypes";
import { useTranslation } from "react-i18next";
import { useGetRecipe } from "../hooks/useGetRecipe";
import InfoIcon from '@mui/icons-material/Info';
import { NUMBER_FIXED_DECIMAL } from "../../../utils/CONST";
import { RecipeDisplay } from "../../components/RecipeDisplay";
import moment from "moment";
import { FORMAT_DATE_DISPLAY, FORMAT_DATE_WITH_NAME, FORMAT_INPUT_DATE } from "../../../utils/getDefualtDates";
import { useReactTableCustom } from "../../../Table/hooks/useReactTableCustom";
import { filterByValue } from "../../../utils/filterByValue";
import { GenerateFiltersForTableDialog } from "../../../Table/GenerateFiltersForTable/GenerateFiltersForTableDialog";
import { useGetLabel } from "../hooks/useGetLabel";
import { usePrintPdfHook } from "../../../components/PrintPdfComponent/hooks/usePrintPdfHook";
import { TaskItemToPrintInterface,  } from "../types/TaskToPrint";
import { DebouncedInput } from "../../../components/DebouncedInput/DebouncedInput";
import { SelectedBranchId } from "../../../GlobalBranch/GlobalBranchState";
import {  HiPrinter } from "react-icons/hi2";
import { CiStickyNote } from "react-icons/ci";
import { Autocomplete, Popover, TextField } from "@mui/material";
function useTaskManagementTable() {
  const { t } = useTranslation();
  const task_management_grouped = useAtomValue(taskManagementGroupedAtom);
  const [sorting, setSorting] = useState<SortingState>([]);
  const [expanded, setExpanded] = useState<ExpandedState>({})
  const [search, setSearch] = useState('')
  const get_recipe_mutation = useGetRecipe({ onRecipeSuccess: () => { } })
  const recipe_object_for_display = useAtomValue(RecipeObjectSchemaForDisplayAtom);
  const task_management_get_dates_list_range = useAtomValue(
    taskManagementGetDatesListRangeAtom
  );
  const date_list = useAtomValue(taskManagementGetDatesListRangeAtom)

  const set_task_management_selected_item = useSetAtom(taskManagementSelectedItemAtom);
  const columns: ColumnDef<TaskManagementGroupedItemType, any>[] =
    useMemo(() => {
      const basic_columns: ColumnDef<TaskManagementGroupedItemType, any>[] = [
        {
          accessorKey: "end_product",
          header: `${t("result")}`,
          enablePinning: true,
          enableColumnFilter: true,
          cell: (info) => <div
            className="recipe-display-item-container"
            onClick={() => {
              get_recipe_mutation.mutate({
                id: info.row.original.meal_task_id, 
                quantity: info.row.original.quantity,
                index: info.row.index
              })
            }}
          >
            <span>{info.row.original?.end_product}</span>
            <span style={{ position: 'relative' }}>
              <InfoIcon className="recipe-display-info" />
              <div
                className="recipe-display-item">
                {recipe_object_for_display.id === info.row.original.meal_task_id ? <>
                  <RecipeDisplay recipe={recipe_object_for_display.data} end_product={info.row.original.end_product ?? undefined} />
                </> : <></>}
              </div>
            </span>
          </div>,
          filterFn: (row, id, filterValue: string | string[]) => {
            return filterByValue(row, id, filterValue, row.original.end_product ?? '')
          }
        },
        {
          accessorKey: "meal_name",
          header: `${t('meal_name')}`, //, // "מנה",
          enablePinning: true,
          enableColumnFilter: true,
          enableSorting: true,
          filterFn: (row, id, filterValue: string | string[]) => {
            return filterByValue(row, id, filterValue, row.original.meal_name)
          }
        },
        {
          accessorKey: 'parent_meal',
          header: `${t("parent_meal")}`,
          enablePinning: false,
          enableColumnFilter: true,
          filterFn: (row, id, filterValue: string | string[]) => {
            // const parent_meals = new Set();
            return filterByValue(row, id, filterValue, row.original.parent_meal ?? '')
          },
          meta: {
            defaultHidden: true
          }
        },
        {
          accessorKey: 'source_type_name',
          header: `${t("source")}`,
          meta: {
            defaultHidden: true
          },
        },
        {
          accessorKey: "station_name",
          header: `${t('station')}`,
          enablePinning: true,
          enableColumnFilter: true,
          filterFn: (row, id, filterValue: string | string[]) => {
            return filterByValue(row, id, filterValue, row.original.station_name)
          }
        },
        {
          header: `${t('total_amount')}`,// "סה״כ כמות",
          enablePinning: true,
          enableColumnFilter: true,
          accessorKey: 'supply_date',
          filterFn: (row, id, filterValue: number | string | string[]) => {
            return filterByValue(row, id, filterValue, row.original.supply_date)
          },
          cell: (info) => <>{parseFloat(info.row.original.quantity.toFixed(NUMBER_FIXED_DECIMAL))} {info.row.original.measurement_unit}</>,
        },

      ];
      const dates_columns = task_management_get_dates_list_range?.map((date, ) => {
        const column: ColumnDef<TaskManagementGroupedItemType, any> = {
          header: moment(date, FORMAT_INPUT_DATE).format("ddd DD/MM/YYYY"),
          // accessorKey: 'total',
          id: `${date}`,
          enablePinning: false,
          accessorFn: (row) => {
            return row.nested.find((item) => item.date === date)?.value;
          },
          enableResizing: true,
          cell: (info) => {
            // return info.row.original.dates[index].value;
            const index_of_date = info.row.original.nested.findIndex(
              (item) => item.date === date
            );
            return (
              <div
                style={{ cursor: "pointer" }}
                onClick={() => {
                  set_task_management_selected_item({
                    taskGroupIndex: info.row.index,
                    nestedIndex: index_of_date,
                  });
                }}
              >
                {parseFloat(info.row.original.nested[index_of_date]?.value?.toFixed(NUMBER_FIXED_DECIMAL))}
              </div>
            );
          },
        };
        return column;
      });
      return [...basic_columns, ...dates_columns];
    }, [task_management_grouped.length, recipe_object_for_display.id, date_list.length, date_list.at(0) , date_list.at(-1)]);

  const table_hook_custom = useReactTableCustom({
    data: task_management_grouped,
    columns: columns,
    sorting: {
      sortingState: sorting,
      setSortingState: setSorting
    },
    expanded: {
      expanded,
      setExpanded
    },
    searchFilter: {
      setFilterState: setSearch,
      filterState: search
    }
  })
  return { table_hook: table_hook_custom, data: task_management_grouped, columns, searchFilter: {
    setFilterState: setSearch,
    filterState: search
  } };
}

interface TaskManagementTablePropsInterface {
  start_date: string;
  end_date: string;
}

export function TaskManagementTable(props: TaskManagementTablePropsInterface) {
  const task_management_grouped = useAtomValue(taskManagementGroupedAtom);
  const task_management_table = useTaskManagementTable();
  const selected_branch_id = useAtomValue(SelectedBranchId)
  const parent_meals_name = useAtomValue(ParentMealNameAtom);
  const setParentMealsFilter = useSetAtom(SelectedParentMealsAtom)
  const sources_type_list = useAtomValue(SourceTypeAtom)
  const set_selected_sources = useSetAtom(SelectedSourcesAtom)
  const table = task_management_table.table_hook.table;
  const get_labels = useGetLabel()
  const print_tasks = usePrintPdfHook({
    url: '/mes/tasks/print/',
    method: 'POST',
    data: null,
  })
  const {t} = useTranslation();
  const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | null>(null);
  const open = Boolean(anchorEl);
  function printTaskByParentMeal() {
    const arr: TaskItemToPrintInterface[] = [];
        for (const task of table.getFilteredRowModel().rows.map(row => row.original)) {
          for (const nested of task.nested) {
            if (nested.info.length === 0) continue;
            const end_data: Record<string, { date: string, parent_meal: string , quantity: number }> = {};
            for (const source_nested of nested.info) {
              const key = `${source_nested.parent_meal}-${source_nested.date}`;
              if (!(key in end_data)) {
                end_data[key] = {
                  date: source_nested.date,
                  parent_meal: source_nested.parent_meal,
                  quantity: 0,
                }
              }
              end_data[key].quantity += source_nested.quantity;
            }
            arr.push({
              station: task.station_name,
              id: task.meal_task_id,
              quantity: nested.value,
              display_quantity: `${parseFloat(nested.value.toFixed(NUMBER_FIXED_DECIMAL))} ${task.measurement_unit}`,
              date: moment(nested.date, FORMAT_INPUT_DATE).format(FORMAT_DATE_DISPLAY),
              end_product: task.end_product,
              source: Object.values(end_data).map(row => {
                return {
                  quantity: parseFloat(row.quantity.toFixed(NUMBER_FIXED_DECIMAL)).toString(),
                  source_title: `${row.parent_meal} ${moment(row.date, FORMAT_INPUT_DATE).format(FORMAT_DATE_WITH_NAME)} | ${parseFloat(row.quantity.toFixed(NUMBER_FIXED_DECIMAL).toString())} ${task.measurement_unit}`,
                }
              }),
            });
          }
        }
        print_tasks.pdf_mutation.mutate({
          start_date: props.start_date,
          end_date: props.end_date,
          branch: selected_branch_id,
          tasks: arr,
        })
  }
  function printTask() {
    const arr: TaskItemToPrintInterface[] = [];
        for (const task of table.getFilteredRowModel().rows.map(row => row.original)) {
          for (const nested of task.nested) {
            if (nested.info.length === 0) continue;
            arr.push({
              station: task.station_name,
              id: task.meal_task_id,
              quantity: nested.value,
              display_quantity: `${parseFloat(nested.value.toFixed(NUMBER_FIXED_DECIMAL))} ${task.measurement_unit}`,
              date: moment(nested.date, FORMAT_INPUT_DATE).format(FORMAT_DATE_DISPLAY),
              end_product: task.end_product,
              source: nested.info.map(source_nested => {
                return {
                  quantity: parseFloat(source_nested.quantity.toFixed(NUMBER_FIXED_DECIMAL)).toString() ,
                  source_title: `${source_nested.source_name ? ' - ' + source_nested.source_name : ''} (${source_nested.source_id}) ${moment(source_nested.supply_date, FORMAT_INPUT_DATE).format("dddd")} | ${parseFloat(source_nested.quantity.toFixed(NUMBER_FIXED_DECIMAL).toString())} ${source_nested.measurement_unit}`,
                }
              }),
            });
          }
        }
        print_tasks.pdf_mutation.mutate({
          start_date: props.start_date,
          end_date: props.end_date,
          branch: selected_branch_id,
          tasks: arr,
        })
  }
  if (task_management_grouped.length === 0) return <></>
  return <>
    <div style={{ paddingBottom: '1rem', position: "relative"}}>
      <div style={{ display: 'flex', gap: '1rem', alignItems: 'center'}}>
        <DebouncedInput
        value={task_management_table.searchFilter.filterState}
        
        onChange={(v) => task_management_table.searchFilter.setFilterState(v.toString())}
        style={{ height: '2.4rem', border: '1px solid rgba(0,0,0,0.2)', borderRadius: '0.2rem'  }}
        />
        <GenerateFiltersForTableDialog table={table} >

          <>
          <div style={{ padding: '1rem 0.5rem'}} className="flex flex-col gap-2">
            <div>
              <Autocomplete
                  multiple
                  onChange={(event, newValue) => {
                    setParentMealsFilter(newValue ?? [])
                  }}
                  options={parent_meals_name}
                  limitTags={1}
                  sx={{ width: 300,  overflow: 'hidden', border: '1px solid #ccc' }}
                  disableCloseOnSelect
                  renderInput={(params) => <TextField {...params} label={t('parent_meal')} />}
                  defaultValue={table.getColumn('parent_meal')?.getFilterValue() as string[] ?? []}
                />
            </div>
            <div>
              <Autocomplete 
              multiple
              onChange={(event, newValue) => {
                set_selected_sources(newValue ?? [])
              }}
              options={sources_type_list}
              limitTags={1}
              getOptionLabel={(option) => t(option === '' ? 'without' : option)}
              sx={{ width: 300,  overflow: 'hidden', border: '1px solid #ccc' }}
              disableCloseOnSelect
              renderInput={(params) => <TextField {...params} label={t('source')} />}
              defaultValue={table.getColumn('source_type_name')?.getFilterValue() as string[] ?? []}
              />

            </div>

            </div> 
          </>
        </GenerateFiltersForTableDialog>
        <div style={{display:"flex", width: "7rem", justifyContent: "space-around",}}>
        <CiStickyNote 
        style={{ cursor: 'pointer', fontSize: "1.5rem" }}
        onClick={() => {
          const rows = table.getFilteredRowModel().rows.map(row => row.original)
          get_labels.get_mutation_label.mutate(rows)
        }} />
        <Popover open={open}
          onClose={() => {
            setAnchorEl(null)
          }}
                anchorEl={anchorEl}>
                <div className="flex flex-col gap-4 p-4">
                  <button className="btn-unstyled add-btn !w-full" onClick={printTask}>
                      {t('by_source')}
                  </button>
                  <button className="btn-unstyled cancel-btn !w-full !cursor-pointer"  onClick={printTaskByParentMeal} >
                      {t('by_parent_meal')}
                  </button>
                
                </div>
        </Popover>
        <button 
        className="btn-unstyled"
        onClick={(e) => {
            setAnchorEl(e.currentTarget)
          }}>
          <HiPrinter style={{ cursor: 'pointer', fontSize: "1.5rem"}}  /> 
        </button>
        
        {/* <HiPrinter style={{ cursor: 'pointer', fontSize: "1.5rem"}} onClick={printTask} /> 
        <HiPrinter style={{ cursor: 'pointer', fontSize: "2rem"}} onClick={printTaskByParentMeal} />  */}
        </div>
       
        
      </div>
    </div>
    <FabiosGenericTable
      data={task_management_table.data}
      columns={task_management_table.columns}
      custom_hook_table={task_management_table.table_hook}
       />
  </>
}
