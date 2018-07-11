import { Component, OnInit } from '@angular/core';
import { DataService } from '../services/data.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-travels',
  templateUrl: './travels.component.html',
  styleUrls: ['./travels.component.scss']
})
export class TravelsComponent implements OnInit {
  travels$: Object;
  title: string;

  constructor(private data: DataService) { }

  ngOnInit() {
    this.title = 'Travels';

    this.data.getTravels().subscribe(
      data => this.travels$ = data
    );
  }

}
