import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MappingsService } from '../mappings.service';


@Component({
  selector: 'app-mapping-detail',
  templateUrl: './mapping-detail.component.html',
  styleUrls: ['./mapping-detail.component.css']
})
export class MappingDetailComponent implements OnInit {
  mappingDetail: any;
  showRemarks = true;

  constructor(
    private route: ActivatedRoute,
    private mappingsService: MappingsService
  ) { }

  ngOnInit(): void {
    const mappingId = this.route.snapshot.paramMap.get('id');
    if (mappingId) {
      this.mappingsService.getMappingDetail(mappingId).subscribe(detail => {
        this.mappingDetail = detail;
      });
    }
  }

  isProfilePresent(fieldProfiles: any[], profileName: string): boolean {
    const profile = fieldProfiles.find(p => p.name === profileName);
    return !!profile?.present;
  }

}
