import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MappingsService } from '../mappings.service';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';
import { PageEvent } from '@angular/material/paginator';
import { Sort } from '@angular/material/sort';

export interface IProfile {
  Property: string;
  Classification_extra: string;
  Erläuterung: string;
  [key: string]: number | string | boolean;
}
@Component({
  selector: 'app-mapping-detail',
  templateUrl: './mapping-detail.component.html',
  styleUrls: ['./mapping-detail.component.css'],
})
export class MappingDetailComponent implements OnInit {
  mappingDetail: any;
  availableFields: any[] = [];
  editingIndex: number | null = null;
  hoverIndex: number | null = null;
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
        this.mappingDetail = mappingDetail;
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

  handlePageEvent(event: PageEvent) {
    this.pageSize = event.pageSize;
    this.pageIndex = event.pageIndex;
    this.filteredDetail = {
      ...this.mappingDetail,
      fields: this.mappingDetail.fields.slice(
        this.pageSize * this.pageIndex,
        this.pageSize * (this.pageIndex + 1)
      ),
    };
  }

  handleSort(event: Sort) {
    const data = this.filteredDetail.fields?.slice();
    if (!event.active || event.direction === '') {
      this.filteredDetail = data;
      return;
    }

    const sortedData = data.sort((a: IProfile, b: IProfile) => {
      const isAsc = event.direction === 'asc';
      switch (event.active) {
        case 'Property':
          return compare(a.Property, b.Property, isAsc);
        case 'Classification_extra':
          return compare(
            a['Classification_extra'],
            b['Classification_extra'],
            isAsc
          );
        case 'Erläuterung':
          return compare(a.Erläuterung, b.Erläuterung, isAsc);
        default:
          return 0;
      }
    });

    this.filteredDetail = { ...this.filteredDetail, fields: sortedData };
  }

  startEditing(index: number): void {
    this.editingIndex = index;
  }

  cancelEditing() {
    this.editingIndex = null;
  }

  startHover(index: number): void {
    if (this.editingIndex === null) {
      this.hoverIndex = index;
    }
  }

  stopHover(): void {
    this.hoverIndex = null;
  }

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
    this.cancelEditing();
  }
}

function compare(a: number | string, b: number | string, isAsc: boolean) {
  return (a < b ? -1 : 1) * (isAsc ? 1 : -1);
}
