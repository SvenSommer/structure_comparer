import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MappingDetailComponent } from './mapping-detail.component';

describe('MappingDetailComponent', () => {
  let component: MappingDetailComponent;
  let fixture: ComponentFixture<MappingDetailComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [MappingDetailComponent]
    });
    fixture = TestBed.createComponent(MappingDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
