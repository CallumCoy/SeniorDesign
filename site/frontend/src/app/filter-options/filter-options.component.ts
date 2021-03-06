import { Injectable } from '@angular/core';
import { Component, OnInit } from '@angular/core';
import { FilterService } from '../filter.service';
import { ToggleService } from '../toggle.service';

@Injectable({
  providedIn: 'root',
})
@Component({
  selector: 'app-filter-options',
  templateUrl: './filter-options.component.html',
  styleUrls: ['./filter-options.component.css'],
})
export class FilterOptionsComponent implements OnInit {
  refresh: boolean = true;

  constructor(
    private filterService: FilterService,
    private toggleService: ToggleService
  ) {}

  ngOnInit(): void {}

  filter(pinned, named, unamed, problems, datef, dateExtra, datet, operator) {
    this.filterService.filtered = true;
    this.filterService.showPinned(!pinned);
    this.filterService.showNamed(!named);
    this.filterService.showUnamed(!unamed);

    const problemsL = false;
    const problemsM = false;
    const problemsH = false;

    if (problems || problemsL || problemsM || problemsH) {
      this.filterService.showProblems(
        problems,
        problemsL,
        problemsM,
        problemsH
      );
    }
    /*
    if (longitude != 0 || latitude != 0 || raduis != 0) {
      this.filterService.showArea(longitude, latitude, raduis);
    }*/

    if (datef) {
      if (dateExtra) {
        this.filterService.showDate(datef, datet);
      } else {
        this.filterService.showDate(datef, new Date());
      }
    }

    if (operator != '') {
      this.filterService.showOperator(operator);
    }
  }

  reset() {
    this.filterService.reset();
    this.ngOnInit();
  }
}
