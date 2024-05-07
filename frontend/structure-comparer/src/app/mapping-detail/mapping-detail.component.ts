import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MappingsService } from '../mappings.service';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';
export interface IProfile {
  name: string;
  extra: string;
  classification: string;
  remark: string;
  [key: string]: any;
}
@Component({
  selector: 'app-mapping-detail',
  templateUrl: './mapping-detail.component.html',
  styleUrls: ['./mapping-detail.component.css'],
})
export class MappingDetailComponent implements OnInit {
  originalDetail: any;
  mappingDetail: any;
  availableFields: any[] = [];
  editingIndex: number | null | undefined = null;
  hoverIndex: number | null | undefined = null;
  filteredDetail: any;
  // Paginator
  totalLength: number = 0;
  pageSize: number = 10;
  pageIndex: number = 0;
  pageSizeOptions: number[] = [10, 20, 50];

  constructor(
    private route: ActivatedRoute,
    private mappingsService: MappingsService
  ) {}

  ngOnInit(): void {
    const mappingId = this.route.snapshot.paramMap.get('id');
    if (mappingId) {
      this.loadMappingDetail(mappingId);
      this.loadFields(mappingId);
    }
  }

  loadMappingDetail(mappingId: string) {
    this.mappingsService
      .getMappingDetail(mappingId)
      .pipe(
        catchError((err) => {
          console.error('Error loading mapping detail', err);
          return of({});
        })
      )
      .subscribe((mappingDetail) => {
        this.totalLength = mappingDetail.fields.length;
        this.originalDetail = mappingDetail;
        this.mappingDetail = this.originalDetail;
        this.filteredDetail = {
          ...mappingDetail,
          fields: mappingDetail.fields.slice(0, this.pageSize),
        };
      });
  }

  loadFields(mappingId: string) {
    this.mappingsService
      .getMappingFields(mappingId)
      .pipe(
        catchError((err) => {
          console.error('Error loading fields', err);
          return of([]);
        })
      )
      .subscribe((fields) => (this.availableFields = fields.fields));
  }

  isProfilePresent(fieldProfiles: any[], profileName: string): boolean {
    const profile = fieldProfiles.find((p) => p.name === profileName);
    return !!profile?.present;
  }

  /**
   * pagination, sort, filtering
   * @param e : Sort | KeyboardEvent | PageEvent
   * @returns new page
   */
  handleTable = (e: any) => {
    const paginator = () => {
      this.pageSize = e.pageSize;
      this.pageIndex = e.pageIndex;
      this.filteredDetail = {
        ...this.mappingDetail,
        fields: this.mappingDetail.fields.slice(
          this.pageSize * this.pageIndex,
          this.pageSize * (this.pageIndex + 1)
        ),
      };
    };

    const sorter = () => {
      const data = this.filteredDetail.fields;
      if (!e.active || e.direction === '') {
        this.filteredDetail = { ...this.filteredDetail, fields: data };
        return;
      }
      const sortedData = data.sort((a: IProfile, b: IProfile) => {
        const isAsc = e.direction === 'asc';
        const otherCondition = (t: any) =>
          t['profiles'].find((profile: any) => profile.name === e.active)
            .present;

        switch (e.active) {
          case 'name':
          case 'remark':
            return compare(a[e.active], b[e.active], isAsc);
          case 'extra':
            return compare(
              a['classification'] + a['extra'],
              b['classification'] + b['extra'],
              isAsc
            );
          default:
            return compare(otherCondition(a), otherCondition(b), isAsc);
        }
      });

      this.filteredDetail = {
        ...this.filteredDetail,
        fields: sortedData,
      };
    };

    const filter = () => {
      const val = (e.target as HTMLInputElement).value.trim().toLowerCase();
      const filterCond = (record: IProfile) => {
        return (
          !val.length ||
          record.name.toLowerCase().indexOf(val) >= 0 ||
          record.remark.toLowerCase().indexOf(val) >= 0 ||
          record.classification.toLowerCase().indexOf(val) >= 0 ||
          record.extra?.toLowerCase().indexOf(val) >= 0
        );
      };
      this.mappingDetail = {
        ...this.mappingDetail,
        fields: this.originalDetail.fields.filter(filterCond),
      };
      this.totalLength = this.mappingDetail.fields.length;
      this.pageIndex = 0;
      this.filteredDetail = {
        ...this.mappingDetail,
        fields: this.mappingDetail.fields.slice(
          this.pageSize * this.pageIndex,
          this.pageSize * (this.pageIndex + 1)
        ),
      };
    };

    return { paginator, sorter, filter };
  };

  /**
   * start, stop of hovering, editing
   * @param idx : number
   * @returns
   */
  handleEdit = (idx?: number) => {
    const startHover = () => {
      if (this.editingIndex === null) {
        this.hoverIndex = idx;
      }
    };

    const stopHover = () => {
      this.hoverIndex = null;
    };

    const startEdit = () => {
      this.editingIndex = idx;
    };

    const cancelEdit = () => {
      this.editingIndex = null;
    };

    return { startHover, stopHover, startEdit, cancelEdit };
  };

  getClassificationCssClass(classification: string): string {
    const CSS_CLASS: { [key: string]: string } = {
      use: 'row-use',
      not_use: 'row-not-use',
      empty: 'row-empty',
      extension: 'row-extension',
      manual: 'row-manual',
      other: 'row-other',
      copy_from: 'row-copy-from',
      copy_to: 'row-copy-to',
      fixed: 'row-fixed',
      medication_service: 'row-medication-service',
    };
    return CSS_CLASS[classification] || '';
  }

  confirmChanges(field: any) {
    const updateData: any = {};

    switch (field.userClassification) {
      case 'copy_from':
        //It would be nice to also define it this way!
        break;
      case 'copy_to':
        updateData.target = field.targetField;
        break;
      case 'fixed':
        // Seems like there is an ug in the backend, if you want to send two times a different fixed value
        updateData.fixed = field.fixedValue;
        break;
      case 'not_use':
        updateData.target = null;
        break;
      case 'use':
        updateData.target = field.id;
        break;
      case 'empty':
        //This does not work How to get the empty state back?
        updateData.target = '';
        break;
      default:
        console.error('Unknown userClassification:', field.userClassification);
        break;
    }

    console.log('Update Data:', updateData); // Debug-Ausgabe der zu sendenden Daten

    // Senden der Daten ans Backend
    this.mappingsService
      .updateMappingField(this.mappingDetail.id, field.id, updateData)
      .subscribe({
        next: () => {
          this.loadMappingDetail(this.mappingDetail.id);
        },
        error: (err) => console.error('Failed to update field', err),
      });

    // Beenden des Bearbeitungsmodus
    this.handleEdit().cancelEdit();
  }
}

const compare = (a: number | string, b: number | string, isAsc: boolean) => {
  return (a < b ? -1 : 1) * (isAsc ? 1 : -1);
};
