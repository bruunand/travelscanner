import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  age: number;

  constructor() { }

  ngOnInit() {
    this.age = 5;
  }

  onClick() {
    console.log('hi');
  }

}
