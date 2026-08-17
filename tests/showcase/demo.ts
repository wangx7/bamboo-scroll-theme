/**
 * 水墨主题 TypeScript 语法与语义高亮测试范例
 */

// 1. 枚举与常量测试 (赭石矿彩 #845438)
export enum ThemeVariant {
  SHIJIE = 'SHUIMO_SHIJIE',
  ZHUYUN = 'SHUIMO_ZHUYUN'
}

export const DEFAULT_LUMINANCE: number = 0.9234;
export const VERSION_REGEX = /^v\d+\.\d+\.\d+$/;

// 2. 接口与泛型测试 (焦墨粗体 #2A2D33 & 斜体泛型)
export interface CanvasConfig<TData extends Record<string, unknown>> {
  readonly id: string;
  name: string;
  variant: ThemeVariant;
  payload: TData;
  render?: (ctx: CanvasRenderingContext2D) => Promise<void>;
}

export type ResultTuple<T, E = Error> = [T | null, E | null];

// 3. 类与装饰器测试 (焦墨类名 #2A2D33 / 黛蓝方法 #20526F)
function LogExecution(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
  const originalMethod = descriptor.value;
  descriptor.value = async function (...args: any[]) {
    console.log(`[Call] Executing: ${propertyKey}`);
    return await originalMethod.apply(this, args);
  };
}

export class InkWashEngine<T extends { title: string }> {
  private _isInitialized: boolean = false;
  private readonly _canvasId: string;

  constructor(canvasId: string, public readonly options: CanvasConfig<T>) {
    this._canvasId = canvasId;
  }

  @LogExecution
  public async renderScene(data: T): Promise<ResultTuple<string>> {
    try {
      if (!this._isInitialized) {
        // 控制流测试 (朱砂红 #983029)
        await this.init();
      }

      const { title } = data;
      const message = `墨韵流淌: ${title} on ${this._canvasId}`;
      return [message, null];
    } catch (error) {
      return [null, error instanceof Error ? error : new Error(String(error))];
    }
  }

  private async init(): Promise<void> {
    this._isInitialized = true;
  }
}
