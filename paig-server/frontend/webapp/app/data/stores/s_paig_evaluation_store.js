import BaseStore from './base_store';
import MEvaluation from '../models/m_evaluation';

class EvaluationStore extends BaseStore {
    constructor() {
        let baseUrl = 'eval-service/api';
        super({
            type: 'evaluation',
            baseUrl
        });
        this.baseUrl = baseUrl;
    }

    addConfig(data, opts = {}) {
        opts.path = '/target/application';
        opts.recordMapper = (json) => new MEvaluation(json);
        return this.create(data, opts);
    }

    updateConfig(data, opts = {}) {
        opts.path = `/target/application/${data.target_id}`;
        opts.recordMapper = (json) => new MEvaluation(json);
        return this.update(data.target_id, data, opts);
    }

    fetchTargetConfig(data, opts = {}) {
        opts.path = `/target/application`;
        opts.recordMapper = (json) => new MEvaluation(json);
        return this.fetch(data.target_id, opts);
    }

    fetchCategories(data, opts = {}) {
        opts.path = `/eval/categories`;
        opts.recordMapper = (json) => new MEvaluation(json);
        return this.create(data, opts);
    }

    evaluateConfig(id, opts = {}) {
        opts.path= `/eval/${id}/run`;
        opts.recordMapper = (json) => new MEvaluation(json);
        return this.create({}, opts);
    }

    fetchEvaluationConfigs(opts = {}) {
        opts.path = '/config/list';
        opts.recordMapper = (json) => new MEvaluation(json);
        opts.deserialize = (resp) => {
            let {content, ...page} = resp
            this.page = page;
            return content;
        }
        return this.fetchAll('', opts);
    }

    fetchEvaluationReports(opts = {}) {
        opts.path = '/eval/report/list';
        opts.recordMapper = (json) => new MEvaluation(json);
        opts.deserialize = (resp) => {
            let {content, ...page} = resp
            this.page = page;
            return content;
        }
        return this.fetchAll('', opts);
    }

    fetchEvaluationAppsList(opts = {}) {
        opts.path = '/target/application/list';
        opts.recordMapper = (json) => new MEvaluation(json);
        opts.deserialize = (resp) => {
            let {content, ...page} = resp
            this.page = page;
            return content;
        }
        return this.fetchAll('', opts);
    }

    deleteAppTarget(id, opts = {}) {
        opts.path= `/target/application`;
        return this.delete(id, opts);
    }
    
    deleteReport(id, opts = {}) {
        opts.path= `/report`;
        return this.delete(id, opts);
    }

    deleteEvalConfig(id, opts = {}) {
        opts.path= `/config`;
        return this.delete(id, opts);
    }

    reRunReport(id, opts = {}) {
        opts.path= `/report/${id}/rerun`;
        opts.recordMapper = (json) => new MEvaluation(json);
        return this.create({}, opts);
    }

}

const evaluationStore = new EvaluationStore();
export default evaluationStore;