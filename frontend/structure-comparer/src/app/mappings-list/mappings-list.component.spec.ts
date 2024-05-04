import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MappingsListComponent } from './mappings-list.component';

describe('MappingsListComponent', () => {
  let component: MappingsListComponent;
  let fixture: ComponentFixture<MappingsListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [MappingsListComponent]
    });
    fixture = TestBed.createComponent(MappingsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
