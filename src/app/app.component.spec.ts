import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { AppComponent } from './app.component';
import { routes } from './app.routes';

describe('AppComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppComponent],
      providers: [provideRouter(routes)],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('should render the navigation with the menu button', () => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('[aria-label="Abrir menu"]')).toBeTruthy();
  });

  describe('asset()', () => {
    it('resolves a path against the base href', () => {
      const fixture = TestBed.createComponent(AppComponent);
      const app = fixture.componentInstance;
      expect(app.asset('favicon.ico')).toBe('/favicon.ico');
      expect(app.asset('/favicon.ico')).toBe('/favicon.ico');
    });
  });
});
