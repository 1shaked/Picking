import { useMutation } from "@tanstack/react-query";
import HttpClient from "../../../../../app/HttpClient";
import { LabelGeneratorItem } from "../types/LabelGeneratorItem";
import { TaskManagementGroupedArrayType } from "../types/TaskManagementTypes";
import { errorMessage, successMessage } from "../../../../shared/utils/ToastMessage/ToastMessage";
import { t } from "i18next";
import moment from "moment";
import { FORMAT_DATE_DISPLAY, FORMAT_INPUT_DATE } from "../../../utils/getDefualtDates";
import { NUMBER_FIXED_DECIMAL } from "../../../utils/CONST";
import print from "print-js";

export function useGetLabel() {

    const get_mutation_label = useMutation({
        mutationKey: ['get_mutation_label'],
        mutationFn: async (rows : TaskManagementGroupedArrayType) => {
            console.log('info', rows)
            const arr: LabelGeneratorItem[] = []
            for (const row of rows) {
                for (const nested_item of row.nested) {
                    for (const info_item of nested_item.info) {
                        const total_labels = Math.ceil(info_item.label_count)
                        for (let label_index = 0; label_index < total_labels; label_index++) {
                            const itemToAdd: LabelGeneratorItem = {
                                date: moment(info_item.date, FORMAT_INPUT_DATE).format(FORMAT_DATE_DISPLAY) ?? '',
                                endProduct: info_item.end_product ?? '',
                                labelCount: (label_index + 1).toString() ?? '1', 
                                order: `${info_item.source_name?.slice(0, 10) ?? ''} ${moment(info_item.supply_date, FORMAT_INPUT_DATE).format("dd") ?? ''}`, 
                                source: "",
                                parentMeal: info_item.parent_meal,
                                quantity: `${parseFloat(info_item.quantity?.toString() ?? '0').toFixed(NUMBER_FIXED_DECIMAL).toString()} ${info_item.measurement_unit}`, 
                                resource: info_item.station_name, 
                                //"identifier": item.identifier, // optional
                                totalLabels: total_labels.toString(), // item.total_labels?.toString() ?? '1'
                            }
                            arr.push(itemToAdd)
                        }
                    }
                }
            }
            const respond = await HttpClient.postBlob(`/mes/work-order-changes/create-labels/`, arr)
            const blob = new Blob([respond.data], { type: 'application/pdf' });
            const url = window.URL.createObjectURL(blob);
            print({
                printable: url,
                type: 'pdf',
            });
            // window.open(url);

        },
        onSuccess: (data) => {
            console.log('success', data)
            successMessage(t('label_printed_successfully'))
        },
        onError: (error) => {
            console.log('error', error);
            errorMessage(t('error_printing_label'))
        }
    })
    return {
        get_mutation_label
    }
}